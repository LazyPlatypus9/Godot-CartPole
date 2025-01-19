using System;
using Godot;
using System.Net.WebSockets;
using Newtonsoft.Json;
using System.Threading.Tasks;
using System.Text;
using System.Threading;
using Utility;
using static GlobalEnums;

namespace Components
{
    [GlobalClass]
    public partial class HitBox : Area2D
    {
        public override void _Ready()
        {
            AddEvents();
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
            Global.Instance.SendToServer(new WebSocketMessage(MessageTypeEnum.TERMINATION));
        }
    }
}