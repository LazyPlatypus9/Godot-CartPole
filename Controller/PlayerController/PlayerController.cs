using Components;
using Godot;
using System;

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
    }

    public override void _PhysicsProcess(double delta)
	{
		Vector2 velocity = Velocity;

		// Get the input direction and handle the movement/deceleration.
		// As good practice, you should replace UI actions with custom gameplay actions.
		Vector2 direction = Input.GetVector(GlobalEnums.InputsEnum.move_left.ToString(), 
											GlobalEnums.InputsEnum.move_right.ToString(), 
											GlobalEnums.InputsEnum.move_up.ToString(), 
											GlobalEnums.InputsEnum.move_down.ToString());
		
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

		Velocity = velocity;
		
		MoveAndSlide();
	}
}
