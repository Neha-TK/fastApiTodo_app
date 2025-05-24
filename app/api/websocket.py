# from fastapi import WebSocket, APIRouter, WebSocketDisconnect

# router = APIRouter()

# active_connections = []

# @router.websocket("/ws/todo")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     active_connections.append(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Echo received message (for testing)
#             for connection in active_connections:
#                 await connection.send_text(f"You said: {data}")
#     except WebSocketDisconnect:
#         active_connections.remove(websocket)





# from fastapi import WebSocket, APIRouter, WebSocketDisconnect

# router = APIRouter()

# active_connections = []

# @router.websocket("/ws/todo")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     active_connections.append(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Send to all except sender
#             for connection in active_connections:
#                 if connection != websocket:
#                     await connection.send_text(f"User says: {data}")
#     except WebSocketDisconnect:
#         active_connections.remove(websocket)




# from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Query
# from typing import List, Dict
# import uuid

# router = APIRouter()

# # We'll store both the websocket and the username
# active_connections: List[Dict] = []

# @router.websocket("/ws/todo")
# async def websocket_endpoint(websocket: WebSocket, username: str = Query(default=None)):
#     await websocket.accept()
    
#     # Assign a random ID if username not provided
#     if not username:
#         username = f"User_{str(uuid.uuid4())[:8]}"

#     # Add to active connections
#     active_connections.append({"socket": websocket, "username": username})
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Send message to all *other* users
#             for conn in active_connections:
#                 if conn["socket"] != websocket:
#                     await conn["socket"].send_text(f"{username} says: {data}")
#     except WebSocketDisconnect:
#         active_connections[:] = [conn for conn in active_connections if conn["socket"] != websocket]






from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()  

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

router = APIRouter()
active_connections: List[Dict] = []

def get_username_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

@router.websocket("/ws/todo")
async def todo_websocket(websocket: WebSocket, token: str = Query(...)):
    username = get_username_from_token(token)
    if not username:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    active_connections.append({"socket": websocket, "username": username})
    print(f"{username} connected.")

    try:
        while True:
            message = await websocket.receive_text()
            for conn in active_connections:
                if conn["username"] != username:
                    await conn["socket"].send_text(f"{username}: {message}")
    except WebSocketDisconnect:
        active_connections[:] = [
            conn for conn in active_connections if conn["socket"] != websocket
        ]
        print(f"{username} disconnected.")
