from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    experience: int
    status: str


# Node 1
def evaluate_candidate(state: State):

    exp = state["experience"]

    if exp > 7:
        status = "Selected"

    elif exp >= 5:
        status = "Waitlisted"

    else:
        status = "Rejected"

    return {
        "status": status
    }


# Create Graph
builder = StateGraph(State)

builder.add_node(
    "evaluation_node",
    evaluate_candidate
)

builder.add_edge(
    START,
    "evaluation_node"
)

builder.add_edge(
    "evaluation_node",
    END
)

graph = builder.compile()



# Multiple Candidates
while True:

    name = input("\nEnter Candidate Name (or exit): ")

    if name.lower() == "exit":
        print("Exiting Recruitment System...")
        break

    experience = int(
        input("Enter Experience (years): ")
    )

    result = graph.invoke(
        {
            "name": name,
            "experience": experience,
            "status": ""
        }
    )
    
    print(result)
    print("\n===== RESULT =====")
   
    print(f"Candidate : {result['name']}")
    print(f"Experience: {result['experience']} years")
    print(f"Status    : {result['status']}")