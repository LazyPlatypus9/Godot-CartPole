using Components.StateMachine;
using Godot;
using Utility;
using static GlobalEnums;

namespace Controller.PlayerController.StartingState
{
    public partial class Observe : PlayerState
    {
        [Export]
        private State SendState;

        public override void Enter()
        {
            
        }

        public override void Exit()
        {
            
        }

        public override State PhysicsProcess(double delta)
        {
            return null;
        }

        public override State Process(double delta)
        {
            Global.Instance.SendToServer(new WebSocketMessage(MessageTypeEnum.FEEDBACK, new CartState(Parent.Pendulum.Rotation, Parent.Position.X, Parent.Velocity.X, Parent.Pendulum.AngularVelocity)));
        
            return SendState;
        }

        public override State UnhandledInput(InputEvent @event)
        {
            return null;
        }
    }
}