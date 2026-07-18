from fastapi import APIRouter, HTTPException

from app.api.chat_schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/message", response_model=ChatResponse)
def send_message(request: ChatRequest) -> ChatResponse:
    try:
        # Pass the extracted session_id and message to our new service
        result = ChatService.process_message(request.session_id, request.message)
        return ChatResponse(**result)
    except ValueError as exc:
        # 🔥 THE TRAP IS DISARMED! This print statement forces the 400 error into your terminal log.
        print(f"🔥 Route Validation/Value Error (400): {exc}") 
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        print(f"Chat Route Error (500): {exc}") 
        raise HTTPException(status_code=500, detail="Unable to process the chat message.") from exc