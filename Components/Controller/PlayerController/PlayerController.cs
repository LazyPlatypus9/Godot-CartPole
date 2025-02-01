using Components;
using Components.StateMachine;
using Godot;
using System;
using Utility;
using Utility.MessengerMessages;
using static GlobalEnums;

public partial class PlayerController : CharacterBody2D
{
	[Export]
	public float Speed = 15.0f;

	public Pendulum Pendulum { get; private set; }

	public StateManager StateManager { get; private set; }

	public bool ServerReady { get; private set; } = false;

	// Get the gravity from the project settings to be synced with RigidBody nodes.
	public float gravity = ProjectSettings.GetSetting("physics/2d/default_gravity").AsSingle();

    public override void _Ready()
    {
       	Pendulum = GetNode<Pendulum>(PendulumNaming.OBJECT_NAME);
		StateManager = GetNode<StateManager>(GlobalNaming.STATE_MANAGER);

		Messenger.Default.Register<MoveCart>(this, MoveCart);
		Messenger.Default.Register<AgentCommand>(this, AgentCommand);
    }

    public override void _ExitTree()
    {
        Messenger.Default.Unregister<MoveCart>(this, MoveCart);
		Messenger.Default.Unregister<AgentCommand>(this, AgentCommand);
    }

    public override void _Process(double delta)
    {
        StateManager._Process(delta);
    }

	public override void _UnhandledInput(InputEvent @event)
    {
        StateManager._UnhandledInput(@event);
    }

    public override void _PhysicsProcess(double delta)
	{
		MoveAndSlide();

		StateManager._PhysicsProcess(delta);
	}

	private void MoveCart(MoveCart moveCart)
	{
		InputEventKey input = new InputEventKey();

		switch (moveCart.InputsEnum)
		{
			case InputsEnum.MOVE_LEFT:
				input.Keycode = Key.A;

				break;
			case InputsEnum.MOVE_RIGHT:
				input.Keycode = Key.D;

				break;
		}

		Logger.Instance.Trace($"Moving {moveCart.InputsEnum}", Logger.LogColor.Yellow);

		input.Pressed = true;

		Input.ParseInputEvent(input);
	}

	private void AgentCommand(AgentCommand agentCommand)
	{
		if (agentCommand.Command == AgentCommandEnum.SERVER_READY)
		{
			ServerReady = true;
		}
	}
}
