using System;
using Godot;
using System.Net.WebSockets;
using Newtonsoft.Json;
using System.Threading.Tasks;
using System.Text;
using System.Threading;

namespace Components
{
    [GlobalClass]
    public partial class HitBox : Area2D
    {
        public ClientWebSocket Client { get; private set; }

        public override void _Ready()
        {
            StartClient();

            AddEvents();
        }

        private async void StartClient()
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

                Console.WriteLine($"Received message from server: {Encoding.UTF8.GetString(receiveBuffer, 0, result.Count)}");
            }
        }

        private async void SendToServer(string data)
        {
            var message = Encoding.UTF8.GetBytes(data);

            await Client.SendAsync(new ArraySegment<byte>(message), WebSocketMessageType.Text, true, CancellationToken.None);
        }

        public override void _ExitTree()
        {
            RemoveEvents();
        }

        public virtual void AddEvents()
		{
			AreaEntered += OnHit;
		}

		public virtual void RemoveEvents()
		{
			AreaEntered -= OnHit;
		}

        private void OnHit(Area2D area2D)
        {
            SendToServer("hit");
        }
    }
}