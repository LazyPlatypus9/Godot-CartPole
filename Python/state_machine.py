from websocket_message import WebSocketMessage
from model import Model
from global_enum import MessageTypeEnum
from states import StartState

class StateMachine(object):
    def __init__(self, model: Model, websocket):
        self.state = StartState(model, websocket)

    async def on_event(self, web_socket_message: WebSocketMessage):
        self.state = await self.state.on_event(web_socket_message)