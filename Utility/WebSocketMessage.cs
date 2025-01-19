using System.Security.Cryptography.X509Certificates;
using static GlobalEnums;

namespace Utility
{
    /// <summary>
    /// Yes, this class does not follow standard C# styling. The reason being that
    /// this class will be used far less often than its Python counterpart therefore
    /// in the war of style choices Python won. The Python and C# classes need to
    /// hard match for the JSON mapping to work.
    /// </summary>
    public class WebSocketMessage
    {
        /// <summary>
        /// JSON deserializer needs the default constructor
        /// </summary>
        public WebSocketMessage() {}

        public WebSocketMessage(MessageTypeEnum messageTypeEnum)
        {
            message_type = (int)messageTypeEnum;
        }


        public WebSocketMessage(MessageTypeEnum messageTypeEnum, string content)
        {
            message_type = (int)messageTypeEnum;
            this.content = content;
        }

        public int message_type { get; set; }

        public string content { get; set; }
    }
}