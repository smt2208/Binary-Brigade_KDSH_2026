"""
LangGraph Agent for Corrective RAG Workflow
Implements a multi-step reasoning process to verify character backstory consistency
"""

from typing import TypedDict, List, Literal
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langchain_community.vectorstores import PathwayVectorClient

# Import configuration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    PATHWAY_HOST, PATHWAY_PORT_CASTAWAYS, PATHWAY_PORT_MONTE_CRISTO,
    BOOK_NAMES, LLM_MODEL, LLM_TEMPERATURE, RETRIEVAL_K
)
from src.prompts import (
    CREATE_QUERIES_SYSTEM, CREATE_QUERIES_USER,
    GENERATE_VERDICT_SYSTEM, GENERATE_VERDICT_USER
)


# Pydantic model for structured verdict output
class VerdictOutput(BaseModel):
    """Structured output for backstory verification verdict"""
    verdict: Literal["consistent", "contradict"] = Field(
        description="Whether the backstory is consistent with the novel or contradicts it"
    )
    rationale: str = Field(
        description="2-3 sentences explaining the decision with specific evidence"
    )


# Define the agent state
class State(TypedDict):
    backstory: str
    character: str
    book_name: str  # Book name to route to correct vector store
    queries: List[str]
    retrieved_docs: List[Document]
    final_answer: str  # Formatted verdict output
    verdict: str  # Direct verdict: "consistent" or "contradict"


vector_client_castaways = PathwayVectorClient(host=PATHWAY_HOST, port=PATHWAY_PORT_CASTAWAYS)
vector_client_monte_cristo = PathwayVectorClient(host=PATHWAY_HOST, port=PATHWAY_PORT_MONTE_CRISTO)

BOOK_VECTOR_CLIENTS = {
    BOOK_NAMES["castaways"]: vector_client_castaways,
    BOOK_NAMES["monte_cristo"]: vector_client_monte_cristo,
}

llm_advanced = ChatOpenAI(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
)

llm_standard = ChatOpenAI(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
)


def create_queries(state: State) -> State:
    prompt = ChatPromptTemplate.from_messages([
        ("system", CREATE_QUERIES_SYSTEM),
        ("user", CREATE_QUERIES_USER)
    ])
    
    chain = prompt | llm_advanced
    response = chain.invoke({
        "character": state["character"],
        "backstory": state["backstory"]
    })
    
    content = response.content if isinstance(response.content, str) else str(response.content)
    queries = [q.strip() for q in content.split('\n') if q.strip()]
    
    state["queries"] = queries 
    print(f"🔍 Generated {len(queries)} queries: {queries}")
    return state


def retrieve_evidence(state: State) -> State:
    all_docs = []
    
    book_name = state.get("book_name", "")
    vector_client = BOOK_VECTOR_CLIENTS.get(book_name)
    
    if vector_client is None:
        print(f"⚠️ Unknown book: {book_name}. Available books: {list(BOOK_VECTOR_CLIENTS.keys())}")
        state["retrieved_docs"] = []
        return state
    
    print(f"📚 Routing to vector store for: {book_name}")
    
    for query in state["queries"]:
        docs = vector_client.similarity_search(query=query, k=RETRIEVAL_K)
        all_docs.extend(docs)
    
    unique_docs = []
    seen_content = set()
    for doc in all_docs:
        if doc.page_content:
            content_hash = hash(doc.page_content[:100])
            if content_hash not in seen_content:
                unique_docs.append(doc)
                seen_content.add(content_hash)
    
    state["retrieved_docs"] = unique_docs
    print(f"🔍 Retrieved {len(unique_docs)} unique document chunks")
    return state


def generate_verdict(state: State) -> State:
    evidence_text = "\n\n---\n\n".join([
        f"[Evidence {i+1}]\n{doc.page_content}" 
        for i, doc in enumerate(state["retrieved_docs"])
    ])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", GENERATE_VERDICT_SYSTEM),
        ("user", GENERATE_VERDICT_USER)
    ])
    
    structured_llm = llm_standard.with_structured_output(VerdictOutput)
    chain = prompt | structured_llm
    
    result = chain.invoke({
        "character": state["character"],
        "backstory": state["backstory"],
        "evidence": evidence_text
    })
    
    verdict = result["verdict"] if isinstance(result, dict) else result.verdict
    rationale = result["rationale"] if isinstance(result, dict) else result.rationale
    
    state["verdict"] = verdict
    state["final_answer"] = rationale  # Store only the rationale, no prefix
    print(f"⚖️ Final verdict: {verdict}")
    return state


def build_graph():
    workflow = StateGraph(State)
    
    workflow.add_node("create_queries", create_queries)
    workflow.add_node("retrieve_evidence", retrieve_evidence)
    workflow.add_node("generate_verdict", generate_verdict)
    
    workflow.add_edge(START, "create_queries")
    workflow.add_edge("create_queries", "retrieve_evidence")
    workflow.add_edge("retrieve_evidence", "generate_verdict")
    workflow.add_edge("generate_verdict", END)
    
    return workflow.compile()


graph = build_graph()


if __name__ == "__main__":
    print("🧪 Testing the agent graph...")
    
    result = graph.invoke({
        "backstory": "The character was born in Paris and later moved to London.",
        "character": "Test Character",
        "book_name": BOOK_NAMES["monte_cristo"],
        "queries": [],
        "retrieved_docs": [],
        "final_answer": "",
        "verdict": ""
    })
    print("\n" + "="*50)
    print("RESULT:", result["final_answer"])
    print("VERDICT:", result["verdict"])
