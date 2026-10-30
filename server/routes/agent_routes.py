"""Agent interaction routes: connects UI to central ReAct AgentExecutor."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from database.connection import get_db
from database.models import AgentTrace, User
from server.auth import get_current_user
from server.schemas.api_models import AgentQueryRequest, AgentQueryResponse
from agent.core import AgentExecutor
from agent.llm import LLM, DryRunLLM
from tools import build_tools
import os

router = APIRouter(prefix="/api/agent", tags=["ReAct Agent"])


@router.post("/query", response_model=AgentQueryResponse)
def query_agent(
    req: AgentQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # If API key is present use LLM, else DryRunLLM
        if os.environ.get("GEMINI_API_KEY") and not os.environ.get("AGENTX_DRY_RUN"):
            try:
                llm = LLM()
            except Exception:
                llm = DryRunLLM()
        else:
            llm = DryRunLLM()

        executor = AgentExecutor(llm, build_tools())
        answer, trace = executor.run(req.query, verbose=False)

        # Store trace in database
        trace_record = AgentTrace(
            student_id=current_user.id,
            query=req.query,
            final_answer=answer,
            trace_json=trace
        )
        db.add(trace_record)
        db.commit()

        return {"answer": answer, "trace": trace}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution error: {e}")
