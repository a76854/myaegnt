import contextlib

from myagent.agent.agent import Agent
from myagent.core.config import get_settings

with contextlib.suppress(ImportError):
    # 导入即生效：让 input() 走 GNU readline 的行编辑，按字符/列宽删除并整行重绘。
    # 不导入时 input() 只在 canonical mode 下按字节退格，汉字（3 字节/2 列）会残留半个字形。
    # Windows 上无 readline，ImportError 被忽略，退回原有行为。
    import readline  # noqa: F401


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

