using System;
using System.Diagnostics;

public sealed class Logger 
{
    public enum LogColor 
    {
        Red,
        Green,
        Yellow,
        Blue,
        Purple,
        Cyan
    }

    private static Logger _instance = null;

    private const string RED = "\u001b[1;31m";
    private const string GREEN = "\u001b[1;32m";
    private const string YELLOW = "\u001b[1;33m";
    private const string BLUE = "\u001b[1;34m";
    private const string PURPLE = "\u001b[1;35m";
    private const string CYAN = "\u001b[1;36m";

    private static readonly object padlock = new object();

    Logger() { }

    public static Logger Instance
    {
        get
        {
            lock (padlock)
            {
                if (_instance == null)
                {
                    _instance = new Logger();
                }

                return _instance;
            }
        }
    }

	public void Trace(string message, LogColor logColor)
    {
        string selectedColor = "";

        switch (logColor)
        {
            case LogColor.Blue:
                selectedColor = BLUE;

                break;
            case LogColor.Cyan:
                selectedColor = CYAN;

                break;
            case LogColor.Green:
                selectedColor = GREEN;

                break;
            case LogColor.Purple:
                selectedColor = PURPLE;

                break;
            case LogColor.Red:
                selectedColor = RED;

                break;
            case LogColor.Yellow:
                selectedColor = YELLOW;

                break;
        }

        Console.ForegroundColor = ConsoleColor.Green;
        Debug.WriteLine(selectedColor + $"{DateTime.Now}: {message}");
    }
}