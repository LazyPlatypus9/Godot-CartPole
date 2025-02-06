using Godot;
using System;

namespace Components.StateMachine
{
    [GlobalClass]
    public abstract partial class PlayerState : AgentState
    {
        [Export]
        public new PlayerController Parent { get; set; }
    }
}