using System;
using System.Numerics;
using System.Security.Cryptography.X509Certificates;
using static GlobalEnums;

namespace Utility
{
    
    public class WebSocketMessage
    {
        /// <summary>
        /// JSON deserializer needs the default constructor
        /// </summary>
        public WebSocketMessage() {}

        public WebSocketMessage(MessageTypeEnum messageTypeEnum, string content = null)
        {
            message_type = (int)messageTypeEnum;

            if (content == null)
            {
                this.content = messageTypeEnum.ToString();
            }
        }

        public WebSocketMessage(MessageTypeEnum messageTypeEnum, CartState cartState, string content = null)
        {
            message_type = (int)messageTypeEnum;
            cart_state = cartState;

            if (content == null)
            {
                this.content = messageTypeEnum.ToString();
            }
        }

        public int message_type { get; set; }

        public string content { get; set; }

        public CartState cart_state { get; set; } = null;

        public CartDriver cart_driver { get; set; } = null;
    }
}