public static class GlobalEnums
{
    public enum InputsEnum
	{
		MOVE_LEFT,
		MOVE_RIGHT,
		MOVE_UP,
		MOVE_DOWN
	}

	public enum MessageTypeEnum
	{
		TERMINATION,
		PING,
		DATA,
		COMMAND,
		FEEDBACK,
		SERVER_READY,
		CLIENT_READY
	}

	public enum AgentCommandEnum
	{
		RESTART,
		SERVER_READY
	}

	public enum AgentStateEnum
	{
		ACT,
		OBSERVE,
		WAIT
	}
}