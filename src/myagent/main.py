from myagent.core.config import get_settings
from myagent.agent.agent import Agent

def main():
    settings = get_settings()
    agent = Agent(settings)
    messages = []
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the agent loop.")
            break
        messages.append({"role": "user", "content": user_input})
        assistant_message = agent.agent_loop(messages)
        print(f"Assistant: {assistant_message}")



if __name__ == "__main__":
    main()

