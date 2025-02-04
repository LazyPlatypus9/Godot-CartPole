from websocket_message import WebSocketMessage
from model import Model

class State(object):
    def __init__(self, model: Model, websocket):
        print(f'Processing current state: {self}')

        self.model = model
        self.websocket = websocket

    async def on_event(self, web_socket_message: WebSocketMessage):
        pass

    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return self.__class__.__name__