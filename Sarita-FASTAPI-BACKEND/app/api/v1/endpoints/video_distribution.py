from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.services.video_distribution_service import VideoDistributionService, get_distribution_service

router = APIRouter()

class DistributionRequest(BaseModel):
    platforms: List[str]
    video_url: str
    title: str
    description: str

@router.post("/publish")
def publish_video(
    *,
    request_in: DistributionRequest,
    db: Session = Depends(deps.get_db),
    distribution_service: VideoDistributionService = Depends(get_distribution_service),
    current_user = Depends(deps.role_required(["admin_general"])),
):
    """
    Publish a video to one or more social media platforms.
    """
    results = []
    errors = []

    for platform in request_in.platforms:
        try:
            result = distribution_service.publish_video(
                platform=platform,
                video_url=request_in.video_url,
                title=request_in.title,
                description=request_in.description
            )
            results.append(result)
        except Exception as e:
            errors.append({"platform": platform, "error": str(e)})

    if not results and errors:
        raise HTTPException(status_code=500, detail={"message": "All publications failed.", "errors": errors})

    return {"message": "Distribution process completed.", "successes": results, "failures": errors}
