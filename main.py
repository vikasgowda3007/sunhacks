import os
from flask import Flask, request
from flask_cors import CORS
import json
from langgraph.graph import StateGraph, END
from agents import UserInteractionAgent, BookingAgent
from db_manager import Database
from config import get_config
from state import AgentState

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/book', methods=['POST'])
def book_court():
    """Read data from UI and print it"""
    try:
        # Get JSON data from request body
        user_request = request.get_json()
        print(user_request)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return f"Error: {str(e)}", 500

def main():
    """
    Main function to run the sports court booking application.
    This function sets up the database, agents, and the LangGraph workflow,
    then processes a user request to book a court.
    """
    config = get_config()
    db = Database(config)
    db.connect()
    db.setup_database()

    # Initialize agents
    
    user_interaction_agent = UserInteractionAgent()
    booking_agent = BookingAgent(db)

    # Define the workflow
    workflow = StateGraph(AgentState)

    workflow.add_node("user_interaction", user_interaction_agent.process_request)
    workflow.add_node("booking", booking_agent.handle_booking)
    workflow.add_node("handle_error", lambda state: {"final_response": state['error']})

    # Set up the graph edges
    workflow.set_entry_point("user_interaction")
    workflow.add_edge("user_interaction", "booking")

    def decide_next_step(state):
        if state["error"]:
            return "handle_error"
        if not state["available_slots"] and not state['booking_details']:
            return "booking" # Re-prompt or suggest alternatives
        return END

    workflow.add_conditional_edges(
        "booking",
        decide_next_step,
        {
            "handle_error": "handle_error",
            "booking": "user_interaction", # Loop back for more info if needed
            END: END
        }
    )
    
    app = workflow.compile()

    # Example user request
    user_request = {
        #"action": "book_court",
        "user_details": {"name": "Jane Doe", "email": "jane.doe@example.com"},
        "sport": {"football" : "Beginner" },
        "date": "2025-10-15",
        "time": "10:00",
        "is_Individual": True # Individual looking for a match
    }
    
    initial_state = {
        "user_request": user_request,
        "user_id": None,
        "booking_details": None,
        "available_slots": [],
        "final_response": None,
        "error": None,
    }

    final_state = app.invoke(initial_state)

    print("--- Final Response ---")
    print(final_state.get('final_response', 'No response generated.'))
    

    db.disconnect()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
    main()