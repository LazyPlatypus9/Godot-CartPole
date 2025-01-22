using static GlobalEnums;

namespace Utility
{
    public class CartDriver
    {
        public CartDriver() {}

        public CartDriver(InputsEnum movement)
        {
            this.movement = (int)movement;
        }

        public int movement { get; set; } = 0;
    }
}
