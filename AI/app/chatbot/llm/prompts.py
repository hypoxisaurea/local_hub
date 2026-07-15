from langchain_core.prompts import ChatPromptTemplate

from app.chatbot.prompts import ANSWER_PROMPT, SYSTEM_PROMPT


answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", ANSWER_PROMPT),
    ]
)
