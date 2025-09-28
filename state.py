from typing import TypedDict, List, Dict, Optional

class AgentState(TypedDict):
    user_request: Optional[Dict]
    user_id: Optional[str]
    booking_details: Optional[Dict]
    available_slots: List[Dict]
    final_response: Optional[str]
    error: Optional[str]