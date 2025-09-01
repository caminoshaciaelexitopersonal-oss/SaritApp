from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
import models
from app.api import deps
from app.agents.corps.units.platoons.squads.marketing_sargento import get_marketing_sargento_graph

router = APIRouter()

@router.post("/generate-text", response_model=schemas.AgentOutput)
def generate_text(
    *,
    agent_input: schemas.AgentInput,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Invokes the Marketing Sargeant agent to generate text content based on a prompt.
    """
    if not agent_input.prompt:
        raise HTTPException(
            status_code=400,
            detail="The 'prompt' field is required.",
        )

    try:
        # Get the agent graph
        marketing_agent_graph = get_marketing_sargento_graph()

        # Invoke the agent with the user's prompt
        response = marketing_agent_graph.invoke({"input": agent_input.prompt})

        # The response from AgentExecutor is a dict, we're interested in the 'output' key
        output_text = response.get("output", "No output generated.")

        return schemas.AgentOutput(response=output_text)

    except Exception as e:
        # Log the exception details if you have a logger setup
        print(f"Error invoking marketing agent: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request with the content generation agent."
        )
