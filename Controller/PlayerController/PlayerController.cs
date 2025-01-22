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

	public Pendulum Pendulum { get; private set; }

	// Get the gravity from the project settings to be synced with RigidBody nodes.
	public float gravity = ProjectSettings.GetSetting("physics/2d/default_gravity").AsSingle();

    public override void _Ready()
    {
       	Pendulum = GetNode<Pendulum>(PendulumNaming.OBJECT_NAME);

		Messenger.Default.Register<MoveCart>(this, MoveCart);
    }

    public override void _ExitTree()
    {
        Messenger.Default.Unregister<MoveCart>(this, MoveCart);
    }

    public override void _PhysicsProcess(double delta)
	{
		MoveAndSlide();

		Global.Instance.SendToServer(new WebSocketMessage(MessageTypeEnum.DATA, new CartState(Pendulum.Rotation)));
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
	}
}
