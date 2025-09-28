import os
import google.generativeai as genai

class UserInteractionAgent:
    """Agent to handle initial user interaction."""
    def process_request(self, state):
        """Processes the initial user request and gathers necessary information."""
        print("--- User Interaction Agent: Processing Request ---")
        user_request = state["user_request"]
        # In a real app, you would have more sophisticated user session management
        # For this example, we'll extract user details directly.
        state["user_id"] = self._get_or_create_user(state)
        print(f"User ID set to: {state['user_id']}")
        return state

    def _get_or_create_user(self, state):
        # This is a simplified user creation/retrieval function.
        # In a real application, this would involve a database lookup.
        return "user_123" 

class ProficiencyAssessmentAgent:
    """Agent to assess user proficiency using Gemini."""
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Gemini API key is not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def assess_proficiency(self, state):
        """Assesses user proficiency based on their self-description."""
        print("--- Proficiency Assessment Agent: Assessing Proficiency ---")
        description = state["user_request"]["user_details"]["description"]
        prompt = f"""
        Analyze the following user's description of their sports experience and rate their proficiency on a scale of 1 (Beginner) to 5 (Advanced).
        Provide a single integer rating.
        Description: "{description}"
        """
        try:
            response = self.model.generate_content(prompt)
            rating = int(response.text.strip())
            state["proficiency_assessment"] = rating
            print(f"Proficiency assessed as: {rating}")
        except Exception as e:
            print(f"Error during proficiency assessment: {e}")
            state["error"] = "Failed to assess proficiency."
        return state

class BookingAgent:
    """Agent to handle court booking and player matching."""
    def __init__(self, db):
        self.db = db

    def handle_booking(self, state):
        """Handles the core logic for booking a court or matching players."""
        print("--- Booking Agent: Handling Booking ---")
        if state["error"]:
            return state

        request = state["user_request"]
        user_id = state["user_id"]
        proficiency = state["proficiency_assessment"]

        self.db.save_user_proficiency(user_id, proficiency)
        
        if request['players'] == 1:
            # Individual player looking for a match
            available_matches = self.db.find_match(request['sport'], request['date'], request['time'], proficiency)
            if available_matches:
                # For simplicity, we book with the first available match
                match = available_matches[0]
                booking_id = self.db.create_booking(match['court_id'], user_id, request['date'], request['time'])
                self.db.add_player_to_group(booking_id, user_id)
                state["booking_details"] = {"booking_id": booking_id, "status": "confirmed", "match_with": match['user_id']}
                state["final_response"] = f"Booking confirmed! You are matched with another player for {request['sport']} on {request['date']} at {request['time']}."
            else:
                # No matches, so create a new open slot
                available_courts = self.db.check_availability(request['sport'], request['date'], request['time'])
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
            available_courts = self.db.check_availability(request['sport'], request['date'], request['time'])
            if available_courts:
                court_id = available_courts[0]['id']
                booking_id = self.db.create_booking(court_id, user_id, request['date'], request['time'])
                state["booking_details"] = {"booking_id": booking_id, "status": "confirmed"}
                state["final_response"] = f"Court for {request['sport']} booked for {request['players']} players on {request['date']} at {request['time']}."
            else:
                state["available_slots"] = []
                state["error"] = "No available courts at the selected time."
                state["final_response"] = "Sorry, no courts are available at that time. Please try a different time."
        
        return state