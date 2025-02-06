using Godot;
using System;

namespace Components.StateMachine
{
    [GlobalClass]
    public abstract partial class State : Node
    {
        public abstract void Enter();

        public abstract void Exit();

        public abstract State PhysicsProcess(double delta);

        public abstract State Process(double delta);

        public abstract State UnhandledInput(InputEvent @event);
    }
}