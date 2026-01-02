# from fastapi import APIRouter, HTTPException
# from typing import List
# from ..models.message_models import ChatRequest, ChatResponse
# from ..services.chatbot_service import chatbot_service
# from ..core.logging import logger


# router = APIRouter()


# @router.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(chat_request: ChatRequest):
#     """
#     Chat endpoint that processes user queries using RAG
#     """
#     try:
#         result = chatbot_service.process_chat(
#             query=chat_request.message,
#             selected_text=chat_request.selected_text
#         )

#         response = ChatResponse(
#             response=result["response"],
#             conversation_id=result["conversation_id"],
#             sources=result["sources"]
#         )

#         return response

#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# from fastapi import APIRouter, HTTPException
# from typing import List
# from ..models.message_models import ChatRequest, ChatResponse
# from ..services.chatbot_service import chatbot_service
# from ..core.logging import logger

# router = APIRouter()

# @router.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(chat_request: ChatRequest):
#     """
#     Chat endpoint that processes user queries using RAG (Retrieve & Generate).
#     It retrieves relevant content from Qdrant, then uses LLM to generate a response.
#     """
#     try:
#         # Process the chat query through RAG pipeline
#         result = await chatbot_service.process_chat(
#             query=chat_request.message,
#             selected_text=chat_request.selected_text
#         )

#         # Prepare the response object
#         response = ChatResponse(
#             response=result["response"],
#             conversation_id=result["conversation_id"],
#             sources=result["sources"]
#         )

#         return response

#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {e}")
#         # Raise HTTP 500 if anything goes wrong
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from ..models.message_models import ChatRequest, ChatResponse
from ..services.chatbot_service import chatbot_service
from ..core.logging import logger

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """
    Chat endpoint that processes user queries using RAG (Retrieve & Generate).
    Retrieves relevant content from Qdrant, then uses LLM to generate a response.
    """
    try:
        # Use conversation_id if provided, otherwise default
        conversation_id = chat_request.conversation_id or "default_conversation"

        # Process chat query through RAG + LLM
        result = await chatbot_service.process_chat(
            query=chat_request.message,
            selected_text=chat_request.selected_text,
            conversation_id=conversation_id
        )

        # Build response
        return ChatResponse(
            response=result.get("response", "I don't know."),
            conversation_id=result.get("conversation_id", conversation_id),
            sources=result.get("sources", [])
        )

    except Exception as e:
        logger.exception(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
