using Components;
using Godot;
using System;
using Utility;
using Utility.MessengerMessages;
using static GlobalEnums;

public partial class PlayerController : CharacterBody2D
{
	public const float Speed = 300.0f;

	public const float JumpVelocity = -400.0f;

	public Pendulum Pendulum { get; private set; }

	public HitBox HitBox { get; private set; }

	// Get the gravity from the project settings to be synced with RigidBody nodes.
	public float gravity = ProjectSettings.GetSetting("physics/2d/default_gravity").AsSingle();

    public override void _Ready()
    {
       	Pendulum = GetNode<Pendulum>(PendulumNaming.OBJECT_NAME);
		HitBox = GetNode<HitBox>(GlobalNaming.HIT_BOX);

		Messenger.Default.Register<MoveCart>(this, MoveCart);
    }

    public override void _ExitTree()
    {
        Messenger.Default.Unregister<MoveCart>(this, MoveCart);
    }

    public override void _PhysicsProcess(double delta)
	{
		/*Vector2 velocity = Velocity;

		// Get the input direction and handle the movement/deceleration.
		// As good practice, you should replace UI actions with custom gameplay actions.
		Vector2 direction = Input.GetVector(GlobalEnums.InputsEnum.MOVE_LEFT.ToString().ToLower(), 
											GlobalEnums.InputsEnum.MOVE_RIGHT.ToString().ToLower(), 
											GlobalEnums.InputsEnum.MOVE_UP.ToString().ToLower(), 
											GlobalEnums.InputsEnum.MOVE_DOWN.ToString().ToLower());
		
		// runs on input
		if (direction != Vector2.Zero)
		{
			velocity.X = direction.X * Speed;
		}
		// this runs if there is no input happening
		else
		{
			velocity.X = Mathf.MoveToward(Velocity.X, 0, Speed);
		}

		Velocity = velocity;*/
		
		MoveAndSlide();

		Global.Instance.SendToServer(new WebSocketMessage(MessageTypeEnum.DATA, new CartState(Pendulum.Rotation)));
	}

	private void MoveCart(MoveCart moveCart)
	{
		Vector2 velocity = Velocity;

		if (moveCart.InputsEnum == InputsEnum.MOVE_LEFT)
		{
			velocity.X = -1 * Speed;
		}
		else if (moveCart.InputsEnum == InputsEnum.MOVE_RIGHT)
		{
			velocity.X = 1 * Speed;
		}

		Velocity = velocity;
	}
}
