# # from fastapi import WebSocket, WebSocketDisconnect
# # from typing import List
# # import json
# # import logging
# # from ..services.chatbot_service import chatbot_service
# # from ..core.logging import logger
# # from ..models.message_models import WebSocketMessage, WebSocketResponse


# # class WebSocketManager:
# #     def __init__(self):
# #         self.active_connections: List[WebSocket] = []

# #     async def connect(self, websocket: WebSocket):
# #         await websocket.accept()
# #         self.active_connections.append(websocket)

# #     def disconnect(self, websocket: WebSocket):
# #         if websocket in self.active_connections:
# #             self.active_connections.remove(websocket)

# #     async def send_personal_message(self, message: dict, websocket: WebSocket):
# #         await websocket.send_text(json.dumps(message))

# #     async def broadcast(self, message: dict):
# #         for connection in self.active_connections:
# #             try:
# #                 await connection.send_text(json.dumps(message))
# #             except:
# #                 self.disconnect(connection)


# # manager = WebSocketManager()


# # async def websocket_endpoint(websocket: WebSocket):
# #     """
# #     WebSocket endpoint for real-time chat
# #     """
# #     await manager.connect(websocket)
# #     try:
# #         while True:
# #             data = await websocket.receive_text()
# #             try:
# #                 message_data = json.loads(data)
# #                 message = WebSocketMessage(**message_data)

# #                 message_type = message.type

# #                 if message_type == "ping":
# #                     response = WebSocketResponse(
# #                         type="pong",
# #                         content="pong"
# #                     )
# #                     await manager.send_personal_message(response.dict(), websocket)
# #                 elif message_type == "chat":
# #                     query = message.content
# #                     conversation_id = message.conversation_id or "default_conversation"

# #                     if not query:
# #                         error_response = WebSocketResponse(
# #                             type="error",
# #                             content="Query is required"
# #                         )
# #                         await manager.send_personal_message(error_response.dict(), websocket)
# #                         continue

# #                     try:
# #                         # Process the chat using the chatbot service
# #                         result = chatbot_service.process_chat(
# #                             query=query,
# #                             selected_text=message.selected_text
# #                         )

# #                         # Send response back to client
# #                         response = WebSocketResponse(
# #                             type="chat_response",
# #                             content=result["response"],
# #                             sources=result["sources"],
# #                             conversation_id=conversation_id
# #                         )
# #                         await manager.send_personal_message(response.dict(), websocket)

# #                     except Exception as e:
# #                         logger.error(f"Error processing chat message: {e}")
# #                         error_response = WebSocketResponse(
# #                             type="error",
# #                             content=f"Error processing your request: {str(e)}"
# #                         )
# #                         await manager.send_personal_message(error_response.dict(), websocket)
# #                 else:
# #                     error_response = WebSocketResponse(
# #                         type="error",
# #                         content=f"Unknown message type: {message_type}"
# #                     )
# #                     await manager.send_personal_message(error_response.dict(), websocket)

# #             except json.JSONDecodeError:
# #                 error_response = WebSocketResponse(
# #                     type="error",
# #                     content="Invalid JSON format"
# #                 )
# #                 await manager.send_personal_message(error_response.dict(), websocket)
# #             except Exception as e:
# #                 logger.error(f"Error processing WebSocket message: {e}")
# #                 error_response = WebSocketResponse(
# #                     type="error",
# #                     content=f"Error processing message: {str(e)}"
# #                 )
# #                 await manager.send_personal_message(error_response.dict(), websocket)

# #     except WebSocketDisconnect:
# #         manager.disconnect(websocket)
# #         logger.info("WebSocket disconnected")

# from fastapi import WebSocket, WebSocketDisconnect
# from typing import List
# import json
# from ..services.chatbot_service import chatbot_service
# from ..core.logging import logger
# from ..models.message_models import WebSocketMessage, WebSocketResponse


# class WebSocketManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#         logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

#     def disconnect(self, websocket: WebSocket):
#         if websocket in self.active_connections:
#             self.active_connections.remove(websocket)
#             logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

#     async def send_personal_message(self, message: dict, websocket: WebSocket):
#         try:
#             await websocket.send_text(json.dumps(message))
#         except Exception as e:
#             logger.error(f"Failed to send message to client: {e}")
#             self.disconnect(websocket)

#     async def broadcast(self, message: dict):
#         for connection in self.active_connections:
#             await self.send_personal_message(message, connection)


# manager = WebSocketManager()


# async def websocket_endpoint(websocket: WebSocket):
#     """
#     WebSocket endpoint for real-time chat
#     """
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             try:
#                 # Parse and validate incoming message
#                 message_data = json.loads(data)
#                 message = WebSocketMessage(**message_data)

#                 if message.type == "ping":
#                     response = WebSocketResponse(type="pong", content="pong")
#                     await manager.send_personal_message(response.dict(), websocket)

#                 elif message.type == "chat":
#                     query = message.content
#                     conversation_id = message.conversation_id or "default_conversation"

#                     if not query.strip():
#                         error_response = WebSocketResponse(type="error", content="Query is required")
#                         await manager.send_personal_message(error_response.dict(), websocket)
#                         continue

#                     try:
#                         # Process the chat using the chatbot service
#                         result = chatbot_service.process_chat(
#                             query=query,
#                             selected_text=message.selected_text
#                         )

#                         # Send response back to client
#                         response = WebSocketResponse(
#                             type="chat_response",
#                             content=result["response"],
#                             sources=result["sources"],
#                             conversation_id=conversation_id
#                         )
#                         await manager.send_personal_message(response.dict(), websocket)

#                     except Exception as e:
#                         logger.error(f"Error processing chat message: {e}")
#                         error_response = WebSocketResponse(
#                             type="error",
#                             content=f"Error processing your request: {str(e)}"
#                         )
#                         await manager.send_personal_message(error_response.dict(), websocket)

#                 else:
#                     error_response = WebSocketResponse(
#                         type="error",
#                         content=f"Unknown message type: {message.type}"
#                     )
#                     await manager.send_personal_message(error_response.dict(), websocket)

#             except json.JSONDecodeError:
#                 error_response = WebSocketResponse(type="error", content="Invalid JSON format")
#                 await manager.send_personal_message(error_response.dict(), websocket)
#             except Exception as e:
#                 logger.error(f"Unexpected error processing WebSocket message: {e}")
#                 error_response = WebSocketResponse(
#                     type="error",
#                     content=f"Error processing message: {str(e)}"
#                 )
#                 await manager.send_personal_message(error_response.dict(), websocket)

#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

# from fastapi import WebSocket, WebSocketDisconnect
# from typing import List
# import json
# from ..services.chatbot_service import chatbot_service
# from ..core.logging import logger
# from ..models.message_models import WebSocketMessage, WebSocketResponse


# class WebSocketManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#         logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

#     def disconnect(self, websocket: WebSocket):
#         if websocket in self.active_connections:
#             self.active_connections.remove(websocket)
#             logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

#     async def send_personal_message(self, message: dict, websocket: WebSocket):
#         try:
#             await websocket.send_text(json.dumps(message))
#         except Exception as e:
#             logger.error(f"Failed to send message to client: {e}")
#             self.disconnect(websocket)

#     async def broadcast(self, message: dict):
#         for connection in self.active_connections:
#             await self.send_personal_message(message, connection)


# manager = WebSocketManager()


# async def websocket_endpoint(websocket: WebSocket):
#     """
#     WebSocket endpoint for real-time chat using Gemini async agent + RAG
#     """
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             try:
#                 # Parse and validate incoming message
#                 message_data = json.loads(data)
#                 message = WebSocketMessage(**message_data)

#                 if message.type == "ping":
#                     response = WebSocketResponse(type="pong", content="pong")
#                     await manager.send_personal_message(response.dict(), websocket)

#                 elif message.type == "chat":
#                     query = message.content
#                     conversation_id = message.conversation_id or "default_conversation"

#                     if not query.strip():
#                         error_response = WebSocketResponse(type="error", content="Query is required")
#                         await manager.send_personal_message(error_response.dict(), websocket)
#                         continue

#                     try:
#                         # -------------------------------
#                         # Async RAG + Gemini response
#                         # -------------------------------
#                         result = await chatbot_service.process_chat(
#                             query=query,
#                             selected_text=message.selected_text
#                         )

#                         response = WebSocketResponse(
#                             type="chat_response",
#                             content=result["response"],
#                             sources=result["sources"],
#                             conversation_id=conversation_id
#                         )
#                         await manager.send_personal_message(response.dict(), websocket)

#                     except Exception as e:
#                         logger.error(f"Error processing chat message: {e}")
#                         error_response = WebSocketResponse(
#                             type="error",
#                             content=f"Error processing your request: {str(e)}"
#                         )
#                         await manager.send_personal_message(error_response.dict(), websocket)

#                 else:
#                     error_response = WebSocketResponse(
#                         type="error",
#                         content=f"Unknown message type: {message.type}"
#                     )
#                     await manager.send_personal_message(error_response.dict(), websocket)

#             except json.JSONDecodeError:
#                 error_response = WebSocketResponse(type="error", content="Invalid JSON format")
#                 await manager.send_personal_message(error_response.dict(), websocket)
#             except Exception as e:
#                 logger.error(f"Unexpected error processing WebSocket message: {e}")
#                 error_response = WebSocketResponse(
#                     type="error",
#                     content=f"Error processing message: {str(e)}"
#                 )
#                 await manager.send_personal_message(error_response.dict(), websocket)

#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio
from pydantic import ValidationError
from ..services.chatbot_service import chatbot_service
from ..core.logging import logger
from ..models.message_models import WebSocketMessage, WebSocketResponse


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to send message to client: {e}", exc_info=True)
            self.disconnect(websocket)

    async def broadcast(self, message: dict):
        """Send message to all connected clients in parallel"""
        await asyncio.gather(
            *(self.send_personal_message(message, conn) for conn in self.active_connections)
        )


manager = WebSocketManager()


async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat using Gemini async agent + RAG
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Parse incoming message
                message_data = json.loads(data)

                # Validate using Pydantic
                try:
                    message = WebSocketMessage(**message_data)
                except ValidationError as ve:
                    error_response = WebSocketResponse(
                        type="error",
                        content=f"Validation error: {ve.errors()}"
                    )
                    await manager.send_personal_message(error_response.dict(), websocket)
                    continue

                # Ping-Pong
                if message.type == "ping":
                    response = WebSocketResponse(type="pong", content="pong")
                    await manager.send_personal_message(response.dict(), websocket)
                    continue

                # Chat query
                elif message.type == "chat":
                    query = message.content
                    conversation_id = message.conversation_id or "default_conversation"

                    if not query or not query.strip():
                        error_response = WebSocketResponse(
                            type="error",
                            content="Query is required"
                        )
                        await manager.send_personal_message(error_response.dict(), websocket)
                        continue

                    try:
                        # -------------------------------
                        # Async RAG + Gemini response
                        # -------------------------------
                        result = await chatbot_service.process_chat(
                            query=query,
                            selected_text=message.selected_text
                        )

                        # Safe access to response and sources
                        response = WebSocketResponse(
                            type="chat_response",
                            content=result.get("response", "I don't know"),
                            sources=result.get("sources", []),
                            conversation_id=conversation_id
                        )
                        await manager.send_personal_message(response.dict(), websocket)

                    except Exception as e:
                        logger.error(f"Error processing chat message: {e}", exc_info=True)
                        error_response = WebSocketResponse(
                            type="error",
                            content=f"Error processing your request: {str(e)}"
                        )
                        await manager.send_personal_message(error_response.dict(), websocket)

                # Unknown type
                else:
                    error_response = WebSocketResponse(
                        type="error",
                        content=f"Unknown message type: {message.type}"
                    )
                    await manager.send_personal_message(error_response.dict(), websocket)

            except json.JSONDecodeError:
                error_response = WebSocketResponse(type="error", content="Invalid JSON format")
                await manager.send_personal_message(error_response.dict(), websocket)
            except Exception as e:
                logger.error(f"Unexpected error processing WebSocket message: {e}", exc_info=True)
                error_response = WebSocketResponse(
                    type="error",
                    content=f"Error processing message: {str(e)}"
                )
                await manager.send_personal_message(error_response.dict(), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
