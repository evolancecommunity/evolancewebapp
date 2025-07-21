# models.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ButtonClickEvent(BaseModel):
    """
    Pydantic model for the data received when a button is clicked.
    """
    user_id: str = Field(..., description="ID of the user who clicked the button")
    button_name: str = Field(..., description="Name or identifier of the button clicked")
    action_description: Optional[str] = Field(None, description="Optional description of the action performed")

class ButtonClickLog(BaseModel):
    """
    Pydantic model for the data stored in MongoDB.
    Includes a timestamp for when the event occurred.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id") # MongoDB _id
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    button_name: str
    action_description: Optional[str]

    class Config:
        populate_by_name = True # Allows field mapping by alias
        json_encoders = {
            datetime: lambda dt: dt.isoformat() + "Z"  # MongoDB prefers ISO format with Z for UTC
        }

class APIResponse(BaseModel):
    """
    Pydantic model for the API response after a successful button click log.
    """
    message: str
    event_id: str
    timestamp: datetime
