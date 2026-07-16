import asyncio

from .graph.builder import chatbot_graph
from .schemas import ChatMessage


EXIT_COMMANDS = {"/exit", "/quit", "exit", "quit", "q"}


async def ask(message: str, history: list[ChatMessage], language: str | None = None) -> str:
    result = await chatbot_graph.ainvoke(
        {
            "message": message,
            "history": [item.model_dump() for item in history],
            "language": language,
        }
    )
    answer = result.get("answer", "")
    history.append(ChatMessage(role="user", content=message))
    history.append(ChatMessage(role="assistant", content=answer))
    return answer


async def main() -> None:
    history: list[ChatMessage] = []
    print("Local Hub chatbot CLI")
    print("Type /exit to quit.")

    while True:
        message = input("\nYou> ").strip()
        if not message:
            continue
        
        if message.lower() in EXIT_COMMANDS:
            print("안녕히 가세요! 또 봐요.")
            return

        try:
            answer = await ask(message, history)
        except Exception as exc:
            print(f"\nBot> 오류가 발생했습니다: {exc}")
            continue

        print(f"\nBot> {answer}")


if __name__ == "__main__":
    asyncio.run(main())
