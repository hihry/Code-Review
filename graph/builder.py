"""Build and compile the LangGraph state graph."""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from chains.analysis_chain import run_analysis_chain
from chains.review_chain import run_review_chain
from chains.security_chain import run_security_chain
from graph.router import route_after_analysis, route_after_planner
from graph.state import CodeReviewState
from nodes.intake import intake
from nodes.planner import planner


def build_graph():
    """Compile the code review workflow graph."""

    graph = StateGraph(CodeReviewState)

    graph.add_node("intake", intake)
    graph.add_node("planner", planner)
    graph.add_node("analysis_chain", run_analysis_chain)
    graph.add_node("security_chain", run_security_chain)
    graph.add_node("review_chain", run_review_chain)

    graph.add_edge(START, "intake")
    graph.add_edge("intake", "planner")

    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "analysis": "analysis_chain",
            "security": "security_chain",
            "review": "review_chain",
        },
    )

    graph.add_conditional_edges(
        "analysis_chain",
        route_after_analysis,
        {
            "security": "security_chain",
            "review": "review_chain",
        },
    )

    graph.add_edge("security_chain", "review_chain")
    graph.add_edge("review_chain", END)

    return graph.compile()
