from cart_state import CartState

class WebSocketMessage:
    def __init__(self, message_type, content: str, cart_state: CartState):
        self.message_type = message_type
        self.content = content
        self.cart_state = cart_state