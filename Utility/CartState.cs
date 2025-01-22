using Godot;
using static GlobalEnums;

namespace Utility
{
    public class CartState
    {
        public CartState() {}

        public CartState(float poleRotation, Vector2 location)
        {
            pole_rotation = poleRotation;
            x = location.X;
            y = location.Y;
        }

        public float pole_rotation { get; set; }

        public float x { get; set; }

        public float y { get; set; }
    }
}
