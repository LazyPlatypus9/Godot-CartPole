using Components;
using Godot;
using System;
using System.Threading;

public partial class Pendulum : RigidBody2D
{
	public Polygon2D Pole { get; private set; }

	public Polygon2D Weight { get; private set; }

	public CollisionShape2D BodyCollision { get; private set; }

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		BodyCollision = GetNode<CollisionShape2D>(PendulumNaming.BODY_COLLISION);

		Pole = GetNode<Polygon2D>(PendulumNaming.POLE);
		Weight = Pole.GetNode<Polygon2D>(PendulumNaming.WEIGHT);
	}
}
