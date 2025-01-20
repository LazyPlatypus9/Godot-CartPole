using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;

namespace Utility
{
    public class Messenger
    {
        private static readonly object CreationLock = new object();
        private static readonly ConcurrentDictionary<MessengerKey, object> Dictionary = new ConcurrentDictionary<MessengerKey, object>();

        private static Messenger _instance;

        public static Messenger Default
        {
            get
            {
                if (_instance == null)
                {
                    lock (CreationLock)
                    {
                        if (_instance == null)
                        {
                            _instance = new Messenger();
                        }
                    }
                }

                return _instance;
            }
        }

        private Messenger()
        {
        }

        public int Count()
        {
            return Dictionary.Count;
        }

        public void Register<T>(object recipient, Action<T> action)
        {
            var key = new MessengerKey(recipient, $"{recipient.GetHashCode()}{typeof(T).Name}", action);

            Dictionary.TryAdd(key, action);
        }

        public void Unregister<T>(object recipient, Action<T> action)
        {
            object removed;

            var key = new MessengerKey(recipient, $"{recipient.GetHashCode()}{typeof(T).Name}", action);
            
            Dictionary.TryRemove(key, out removed);
        }

        public void Send<T>(T message, int hash)
        {
            IEnumerable<KeyValuePair<MessengerKey, object>> result = from r in Dictionary where r.Key.Key.Equals(hash + typeof(T).Name) select r;

            foreach (var action in result.Select(x => x.Value).OfType<Action<T>>())
            {
                // Send the message to all recipients.
                action(message);
            }
        }

        public void Send<T>(T message)
        {
            IEnumerable<KeyValuePair<MessengerKey, object>> result = from r in Dictionary select r;

            foreach (var action in result.Select(x => x.Value).OfType<Action<T>>())
            {
                // Send the message to all recipients.
                action(message);
            }
        }

        public void Log()
        {
            foreach (var item in Dictionary)
            {
                Logger.Instance.Trace(item.ToString(), Logger.LogColor.Cyan);
            }
        }

        protected class MessengerKey
        {
            public object Recipient { get; private set; }
            public string Key { get; private set; }
            public object Action { get; private set; }

            /// <summary>
            /// Initializes a new instance of the MessengerKey class.
            /// </summary>
            /// <param name="recipient"></param>
            /// <param name="key"></param>
            /// <param name="action"></param>
            public MessengerKey(object recipient, string key, object action)
            {
                Recipient = recipient;
                Key = key;
                Action = action;
            }

            /// <summary>
            /// Determines whether the specified MessengerKey is equal to the current MessengerKey.
            /// </summary>
            /// <param name="other"></param>
            /// <returns></returns>
            protected bool Equals(MessengerKey other)
            {
                return Equals(Recipient, other.Recipient) && Equals(Key, other.Key);
            }

            /// <summary>
            /// Determines whether the specified MessengerKey is equal to the current MessengerKey.
            /// </summary>
            /// <param name="obj"></param>
            /// <returns></returns>
            public override bool Equals(object obj)
            {
                if (ReferenceEquals(null, obj)) return false;
                if (ReferenceEquals(this, obj)) return true;
                if (obj.GetType() != GetType()) return false;

                return Equals((MessengerKey)obj);
            }

            /// <summary>
            /// Serves as a hash function for a particular type. 
            /// </summary>
            /// <returns></returns>
            public override int GetHashCode()
            {
                unchecked
                {
                    return (Recipient != null ? Recipient.GetHashCode() : 0) * 397;
                }
            }
        }
    }
}