import json
from config import CONFIG
from cart_driver import CartDriver
from websocket_message import WebSocketMessage
from cart_state import CartState
from global_enum import InputsEnum, MessageTypeEnum
from state import State

class StartState(State):
    async def on_event(self, web_socket_message: WebSocketMessage):
        if web_socket_message.message_type == MessageTypeEnum.CLIENT_READY.value:
            return CommandState(self.model, self.websocket)
        
        return self
    
class CommandState(State):
    async def on_event(self, web_socket_message: WebSocketMessage):
        if web_socket_message.message_type == MessageTypeEnum.DATA.value:
            print(f"Episode: {self.model.current_episode}, Global Step: {self.model.steps}")

            self.model.steps += 1

            self.model.current_state = CartState(0, 0, 0, 0, web_socket_message.cart_state)

            self.model.action_taken = self.model.get_action(self.model.current_state)

            if self.model.action_taken == InputsEnum.MOVE_LEFT.value:
                await self.websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(0)).__dict__, 
                                                    default=lambda o: o.__dict__))
            else:
                await self.websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.COMMAND.value, str(MessageTypeEnum.COMMAND), None, CartDriver(1)).__dict__, 
                                                default=lambda o: o.__dict__))

            return UpdateNetworkState(self.model, self.websocket)
        
        return self

class UpdateNetworkState(State):
    async def on_event(self, web_socket_message: WebSocketMessage):
        if web_socket_message.message_type == MessageTypeEnum.FEEDBACK.value:
            new_state: CartState = CartState(0, 0, 0, 0, web_socket_message.cart_state)

            reward = self.model.get_reward(new_state)

            done = False

            if reward < 0:
                done = True
            
            self.model.memory.add(self.model.current_state.to_tensor(self.model.DEVICE), self.model.action_taken, reward, new_state.to_tensor(self.model.DEVICE), done)

            if len(self.model.memory.buffer) > CONFIG['training']['batch_size']:
                loss = self.model.optimize_model()

                print(f"Loss: {loss}")
                
                # Update target network periodically
                if self.model.steps % CONFIG['training']['update_rate'] == 0:
                    self.model.target_network.load_state_dict(self.model.policy_network.state_dict())

            print(f"Old state: {self.model.current_state.__dict__}")
            print(f"New state: {new_state.__dict__}")

            self.model.episode_duration += 1

            if done:
                self.model.durations.append(self.model.episode_duration)

                self.model.current_state = None
                self.model.action_taken = None
                self.model.current_episode += 1
                self.model.episode_duration = 0

                await self.websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.TERMINATION.value, str(MessageTypeEnum.TERMINATION), None, CartDriver(0)).__dict__, 
                                                    default=lambda o: o.__dict__))
                    
                await self.websocket.send(json.dumps(WebSocketMessage(MessageTypeEnum.SERVER_READY.value, str(MessageTypeEnum.SERVER_READY), None, None).__dict__))

                return StartState(self.model, self.websocket)

            return CommandState(self.model, self.websocket)
        
        return self