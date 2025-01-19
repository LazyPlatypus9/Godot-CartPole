class WebSocketMessage:
    def __init__(self, message_type, content):
        self.message_type = message_type
        self.content = content