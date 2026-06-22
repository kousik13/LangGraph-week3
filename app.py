from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)


class State(TypedDict):
    topic: str
    
    question: str
    answer: str


def create_question(state: State):

    topic = state["topic"]

    prompt = f"""
    Generate one interview-style question about:
    {topic}

    Return only the question.
    """

    response = llm.invoke(prompt)

    return {
        "question": response.content
    }


def create_answer(state: State):

    question = state["question"]

    prompt = f"""
    Answer the following question in 5 lines:

    {question}
    """

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


builder = StateGraph(State)

builder.add_node(
    "question_node",
    create_question
)

builder.add_node(
    "answer_node",
    create_answer
)

builder.set_entry_point(
    "question_node"
)

builder.add_edge(
    "question_node",
    "answer_node"
)

builder.add_edge(
    "answer_node",
    END
)

graph = builder.compile()

result = graph.invoke(
    {
        "topic": "LangGraph",
        "question": "",
        "answer": ""
    }
)

print("\nQuestion:")
print(result["question"])

print("\nAnswer:")
print(result["answer"])