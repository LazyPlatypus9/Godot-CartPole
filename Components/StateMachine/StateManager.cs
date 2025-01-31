using Godot;
using System;
using System.Diagnostics;
using System.Linq;
using Utility;

namespace Components.StateMachine
{
	[GlobalClass]
	public partial class StateManager : Node
	{
		[Export]
		public State StartingState;

		private State _currentState;

		private void ChangeState(State state)
		{
			if (_currentState != null)
			{
				_currentState.Exit();

				Logger.Instance.Trace($"{Owner.Name} changing from {_currentState.Name} to {state.Name}", Logger.LogColor.Cyan);
			}

			_currentState = state;
			_currentState.Enter();
		}

		#region Godot functions
		// Called when the node enters the scene tree for the first time.
		public override void _Ready()
		{
			ChangeState(StartingState);
		}

		// Called every frame. 'delta' is the elapsed time since the previous frame.
		public override void _Process(double delta)
		{
			State state = _currentState.Process(delta);

			if (state != null)
			{
				ChangeState(state);
			}
		}

        public override void _UnhandledInput(InputEvent @event)
        {
            State state = _currentState.UnhandledInput(@event);

			if (state != null)
			{
				ChangeState(state);
			}
        }

        public override void _PhysicsProcess(double delta)
        {
            State state = _currentState.PhysicsProcess(delta);

			if (state != null)
			{
				ChangeState(state);
			}
        }
		#endregion

		public void Reset()
		{
			_currentState = StartingState;
		}
    }
}