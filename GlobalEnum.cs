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
		READY
	}

	public enum AgentStateEnum
	{
		ACT,
		OBSERVE,
		WAIT
	}
}