from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv

#answer 
# Proficient in Python, React, and Node.js, with a strong background in developing scalable web applications

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

MAX_ATTEMPTS = 3


class State(TypedDict):
    resume: str
    feedback: str
    decision: str
    retry_count: int


SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "react",
    "node",
    "sql",
    "mongodb",
    "mysql",
    "aws",
    "docker",
    "kubernetes",
    "langchain",
    "langgraph",
    "fastapi",
    "machine learning",
    "deep learning",
    "rag",
    "prompt engineering",
    "agentic ai"
]


def review_resume(state: State):

    resume = state["resume"].lower()

    skill_count = 0

    for skill in SKILLS:
        if skill in resume:
            skill_count += 1

    decision = "GOOD"

    # Rule 1: Questions are invalid
    if "?" in resume:
        decision = "BAD"

    # Rule 2: Too short
    elif len(resume) < 50:
        decision = "BAD"

    # Rule 3: Need at least 2 skills
    elif skill_count < 2:
        decision = "BAD"

    print("\nReviewing Resume...")
    print(f"Skills Found: {skill_count}")
    print(f"Decision: {decision}")

    prompt = f"""
    You are an HR recruiter.

    Resume Summary:
    {state['resume']}

    The resume has already been classified as:

    {decision}

    Give feedback in 4-5 lines.
    Do not change the decision.
    """

    response = llm.invoke(prompt)

    return {
        "decision": decision,
        "feedback": response.content
    }


def route(state: State):

    decision = state["decision"]
    retry = state["retry_count"]

    if decision == "BAD" and retry < MAX_ATTEMPTS - 1:
        print("\n❌ Resume is not good enough.")
        return "retry"

    if decision == "BAD" and retry >= MAX_ATTEMPTS - 1:
        print("\n❌ Maximum attempts reached.")
        return "end"

    print("\n✅ Resume looks good.")
    return "end"


def retry_resume(state: State):

    retry = state["retry_count"] + 1

    print(f"\nRetry Count: {retry}")

    new_resume = input(
        "\nImprove your Resume Summary:\n"
    )

    return {
        "resume": new_resume,
        "retry_count": retry
    }


builder = StateGraph(State)

builder.add_node(
    "review",
    review_resume
)

builder.add_node(
    "retry",
    retry_resume
)

builder.add_edge(
    START,
    "review"
)

builder.add_conditional_edges(
    "review",
    route,
    {
        "retry": "retry",
        "end": END
    }
)

builder.add_edge(
    "retry",
    "review"
)

graph = builder.compile()


resume = input(
    "Enter Resume Summary:\n"
)

result = graph.invoke(
    {
        "resume": resume,
        "feedback": "",
        "decision": "",
        "retry_count": 0
    }
)

print("\n===== FINAL RESULT =====")
print(f"Decision : {result['decision']}")

print("\n===== FEEDBACK =====")
print(result["feedback"])