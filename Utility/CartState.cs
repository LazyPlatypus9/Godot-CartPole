namespace Utility
{
    public class CartState
    {
        public CartState() {}

        public CartState(float poleRotation)
        {
            pole_rotation = poleRotation;
        }

        public float pole_rotation { get; set; }
    }
}
