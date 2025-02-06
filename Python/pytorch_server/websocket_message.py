from cart_state import CartState
from cart_driver import CartDriver

class WebSocketMessage:
    def __init__(self, message_type, content: str, cart_state: CartState, cart_driver: CartDriver):
        self.message_type = message_type
        self.content = content
        self.cart_state = cart_state
        self.cart_driver = cart_driver