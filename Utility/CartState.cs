using static GlobalEnums;

namespace Utility
{
    public class CartState
    {
        public CartState() {}

        public CartState(float poleRotation)
        {
            pole_rotation = poleRotation;
        }

        public CartState(InputsEnum movement)
        {
            this.movement = (int)movement;
        }

        public float pole_rotation { get; set; }

        public int movement { get; set; } = 0;
    }
}
