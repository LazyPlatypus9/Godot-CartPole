using Components.StateMachine;
using Godot;
using Utility;
using static GlobalEnums;

namespace Controller.PlayerController.StartingState
{
    public partial class Start : PlayerState
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
            if (Parent.ServerReady)
            {
                Global.Instance.SendToServer(new WebSocketMessage(MessageTypeEnum.CLIENT_READY, new CartState(Parent.Pendulum.Rotation, Parent.Position.X, Parent.Velocity.X, Parent.Pendulum.AngularVelocity)));

                return SendState;
            }

            return null;
        }

        public override State UnhandledInput(InputEvent @event)
        {
            return null;
        }
    }
}