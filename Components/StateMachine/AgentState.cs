using Godot;
using System;

namespace Components.StateMachine
{
    [GlobalClass]
    public abstract partial class AgentState : State
    {
        [Export]
        public CharacterBody2D Parent { get; set; }
    }
}