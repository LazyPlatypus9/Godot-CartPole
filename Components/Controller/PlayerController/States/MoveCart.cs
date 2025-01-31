using Components.StateMachine;
using Godot;
using Utility;
using static GlobalEnums;

namespace Controller.PlayerController.StartingState
{
    public partial class MoveCart : PlayerState
    {
        [Export]
        private State Observe;

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
            return null;
        }

        public override State UnhandledInput(InputEvent @event)
        {
            if (@event is InputEventKey eventKey)
            {
                Vector2 velocity = Parent.Velocity;

                if (eventKey.Keycode == Key.A)
                {
                    velocity.X = -1 * Parent.Speed;
                }
                else if (eventKey.Keycode == Key.D)
                {
                    velocity.X = 1 * Parent.Speed;
                }

                Parent.Velocity = velocity;

                return Observe;
            }
            
            return null;
        }
    }
}