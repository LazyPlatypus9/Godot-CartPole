using System;
using Godot;
using static GlobalEnums;

namespace Utility
{
    public class CartState
    {
        public CartState() {}

        public CartState(float poleRotation, float x, float velocity, float angularVelocity)
        {
            pole_rotation = poleRotation;
            this.x = x;
            this.velocity = velocity;
            angular_velocity = angularVelocity;
        }

        public float pole_rotation { get; set; }

        public float x { get; set; }

        public float velocity { get; set; }

        public float angular_velocity { get; set; }

        public DateTime date { get; set; } = DateTime.Now;
    }
}
