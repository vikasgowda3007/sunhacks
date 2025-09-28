import os
import google.generativeai as genai
from state import AgentState

class UserInteractionAgent:
    """Agent to handle initial user interaction."""
    def __init__(self):
        pass

    def process_request(self, state):
        """Processes the initial user request and gathers necessary information."""
        print("--- User Interaction Agent: Processing Request ---")
        #user_request = state['user_request']
        #state['user_request'] = user_request 
        # In a real app, you would have more sophisticated user session management
        # For this example, we'll extract user details directly.
        state["user_id"] = self._get_or_create_user(state)
        print(f"User ID set to: {state['user_id']}")
        return state

    def _get_or_create_user(self, state):
        # This is a simplified user creation/retrieval function.
        # In a real application, this would involve a database lookup.
        return "user_123" 



class BookingAgent:
    """Agent to handle court booking and player matching."""
    def __init__(self, db):
        self.db = db

    def handle_booking(self, state):
        """Handles the core logic for booking a court or matching players."""
        print("--- Booking Agent: Handling Booking ---")
        if state.get("error"):
            return state

        request = state["user_request"]
        user_id = state["user_id"]
        sport_dict = request['sport']
        sport_name = list(sport_dict.keys())[0]
        proficiency = sport_dict[sport_name]
        email = request['user details']['email']
        name = request['user details']['name']

        self.db.save_user_proficiency(user_id, name, email, proficiency)
        
        if request['is_Individual']:
            # Individual player looking for a match
            available_matches = self.db.find_match(sport_name, request['date'], request['time'], proficiency) # sport.key() => sport, sport.value()=> proficiency
            if available_matches:
                # For simplicity, we book with the first available match
                match = available_matches[0]
                #booking_id = self.db.create_booking(match['court_id'], user_id, request['date'], request['time'])
                booking_id = match.get('id')
                if booking_id is None:
                    print("No 'id' key found in match:", match)
                self.db.add_player_to_group(booking_id, user_id)
                state["booking_details"] = {"booking_id": booking_id, "status": "confirmed", "match_with": match['user_id']}
                state["final_response"] = f"Booking confirmed! You are matched with another player for {request['sport.key()']} on {request['date']} at {request['time']}."
            else:
                # No matches, so create a new open slot
                available_courts = self.db.check_availability(sport_name, request['date'], request['time'])
                if available_courts:
                    court_id = available_courts[0]['id']
                    booking_id = self.db.create_booking(court_id, user_id, request['date'], request['time'], status='pending_match')
                    self.db.add_player_to_group(booking_id, user_id)
                    state["booking_details"] = {"booking_id": booking_id, "status": "pending_match"}
                    state["final_response"] = f"No matches found. We have created an open slot for you on {request['date']} at {request['time']}. We will notify you when another player joins."
                else:
                    state["available_slots"] = []
                    state["error"] = "No available courts at the selected time."
                    state["final_response"] = "Sorry, no courts are available at that time. Please try a different time."
        else: # Group booking
            available_courts = self.db.check_availability(sport_name, request['date'], request['time'])
            if available_courts:
                court_id = available_courts[0]['id']
                booking_id = self.db.create_booking(court_id, user_id, request['date'], request['time'])
                state["booking_details"] = {"booking_id": booking_id, "status": "confirmed"}
                state["final_response"] = f"Court for {sport_name} booked on {request['date']} at {request['time']}."
            else:
                state["available_slots"] = []
                state["error"] = "No available courts at the selected time."
                state["final_response"] = "Sorry, no courts are available at that time. Please try a different time."
        
        return state