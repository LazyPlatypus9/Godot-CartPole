using Components;
using Godot;
using System;
using Utility;
using Utility.MessengerMessages;
using static GlobalEnums;

public partial class PlayerController : CharacterBody2D
{
	[Export]
	public float Speed = 300.0f;

	public const float JumpVelocity = -400.0f;

	public Vector2 OldPosition { get; private set; }

	public float OldRotation { get; private set; }

	public Pendulum Pendulum { get; private set; }

	public AgentStateEnum AgentState { get; private set; }

	public bool CommandMove { get; private set; }

	// Get the gravity from the project settings to be synced with RigidBody nodes.
	public float gravity = ProjectSettings.GetSetting("physics/2d/default_gravity").AsSingle();

    public override void _Ready()
    {
       	Pendulum = GetNode<Pendulum>(PendulumNaming.OBJECT_NAME);

		AgentState = AgentStateEnum.ACT;

		Messenger.Default.Register<MoveCart>(this, MoveCart);

		if (Global.Client != null)
		{
			Global.Instance.SendToServer(new WebSocketMessage(MessageTypeEnum.READY));
		}
    }

    public override void _ExitTree()
    {
        Messenger.Default.Unregister<MoveCart>(this, MoveCart);
    }

    public override void _Process(double delta)
    {
        switch (AgentState)
		{
			case AgentStateEnum.ACT:
				if (Global.Client.State == System.Net.WebSockets.WebSocketState.Open)
				{
					Global.Instance.SendToServer(new WebSocketMessage(MessageTypeEnum.DATA, new CartState(Pendulum.Rotation, Position.X, Velocity.X, Pendulum.AngularVelocity)));

					AgentState = AgentStateEnum.WAIT;
				}

				break;
		}
    }

    public override void _PhysicsProcess(double delta)
	{
		switch (AgentState)
		{
			case AgentStateEnum.OBSERVE:
				MoveAndSlide();

				Global.Instance.SendToServer(new WebSocketMessage(MessageTypeEnum.FEEDBACK, new CartState(Pendulum.Rotation, Position.X, Velocity.X, Pendulum.AngularVelocity)));

				AgentState = AgentStateEnum.ACT;

				break;
		}
	}

	private void MoveCart(MoveCart moveCart)
	{
		Vector2 velocity = Velocity;

		if (moveCart.InputsEnum == InputsEnum.MOVE_LEFT)
		{
			Logger.Instance.Trace("Move left", Logger.LogColor.Blue);

			velocity.X = -1 * Speed;
		}
		else if (moveCart.InputsEnum == InputsEnum.MOVE_RIGHT)
		{
			Logger.Instance.Trace("Move right", Logger.LogColor.Blue);

			velocity.X = 1 * Speed;
		}

		Velocity = velocity;

		AgentState = AgentStateEnum.OBSERVE;
	}
}
