using Godot;
using System;
using Utility;
using Utility.MessengerMessages;
using static GlobalEnums;

public partial class GameScene : Node
{
	public Node2D Start { get; private set; }

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		Start = GetNode<Node2D>(GlobalNaming.START);

		LoadAgent();

		Global.Instance.StartClient();

		Messenger.Default.Register<AgentCommand>(this, AgentCommand);
	}

    public override void _ExitTree()
    {
        Messenger.Default.Unregister<AgentCommand>(this, AgentCommand);
    }

    // Called every frame. 'delta' is the elapsed time since the previous frame.
    public override void _Process(double delta)
	{
	}

	private void LoadAgent()
	{
		Node newScene = GD.Load<PackedScene>(SceneLocations.PLAYER_CONTROLLER).Instantiate();
	
		Start.AddChild(newScene);
	}

	private void RemoveAgent()
	{
		PlayerController playerController = Start.GetNode<PlayerController>(GlobalNaming.PLAYER_CONTROLLER);

		Start.RemoveChild(playerController);

		playerController.Free();
	}

	private void AgentCommand(AgentCommand agentCommand)
	{
		if (agentCommand.Command == AgentCommandEnum.RESTART)
		{
			RemoveAgent();

			LoadAgent();
		}
	}
}
