using System;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading;
using Godot;
using Utility;
using Utility.MessengerMessages;
using static GlobalEnums;

public sealed class Global 
{
    private static Global _instance = null;

    public static ClientWebSocket Client { get; private set; }

    private static readonly object padlock = new object();

	public static Global Instance
    {
        get
        {
            lock (padlock)
            {
                if (_instance == null)
                {
                    _instance = new Global();
                }

                return _instance;
            }
        }
    }

    public async void StartClient()
    {
        if (Client == null || Client.State != WebSocketState.Open)
        {
            int port = 8765;
            Uri uri = new Uri($"ws://localhost:{port}");

            Client = new ClientWebSocket();

            await Client.ConnectAsync(uri, CancellationToken.None);

            // Receive messages from the server asynchronously
            var receiveBuffer = new byte[1024];
            while (Client.State == WebSocketState.Open)
            {
                var result = await Client.ReceiveAsync(new ArraySegment<byte>(receiveBuffer), CancellationToken.None);

                if (result.MessageType == WebSocketMessageType.Close) 
                {
                    break;
                }

                WebSocketMessage translatedMessage = JsonSerializer.Deserialize<WebSocketMessage>(Encoding.UTF8.GetString(receiveBuffer, 0, result.Count));

                Logger.Instance.Trace($"message_type: {translatedMessage.message_type}, content: {translatedMessage.content}", Logger.LogColor.Cyan);
            
                switch ((MessageTypeEnum)translatedMessage.message_type)
                {
                    case MessageTypeEnum.COMMAND:
                        Messenger.Default.Send(new MoveCart() { InputsEnum = (InputsEnum)translatedMessage.cart_driver.movement });
                        break;
                    case MessageTypeEnum.TERMINATION:
                        Messenger.Default.Send(new AgentCommand() { Restart = true });
                        break;
                }
            }
        }
    }

    public async void SendToServer(WebSocketMessage webSocketMessage)
    {
        var message = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(webSocketMessage));

        if (Client.State == WebSocketState.Open)
        {
            try
            {
                await Client.SendAsync(new ArraySegment<byte>(message), WebSocketMessageType.Text, true, CancellationToken.None);
            }
            catch (Exception exception)
            {
                Logger.Instance.Trace(exception.Message, Logger.LogColor.Red);
            }
        }
    }
}