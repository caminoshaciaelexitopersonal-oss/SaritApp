from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import models
from app.api import deps
from app.crud import settings as crud_settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class WhatsAppSettings(BaseModel):
    api_token: str
    phone_number_id: str


class ApiSettings(BaseModel):
    openai_api_key: str
    google_api_key: str
    youtube_refresh_token: str
    meta_user_access_token: str
    facebook_page_id: str


@router.get("/settings/api_keys", response_model=ApiSettings)
def get_api_keys(
    db: Session = Depends(deps.get_db),
    current_user: models.Usuario = Depends(deps.role_required(["admin_general"])),
):
    """
    Retrieve API keys for the Admin General.
    """
    openai_key = crud_settings.get_setting(db, key="openai_api_key")
    google_key = crud_settings.get_setting(db, key="google_api_key")
    youtube_token = crud_settings.get_setting(db, key="youtube_refresh_token")
    meta_token = crud_settings.get_setting(db, key="meta_user_access_token")
    fb_page_id = crud_settings.get_setting(db, key="facebook_page_id")

    return ApiSettings(
        openai_api_key=openai_key.value if openai_key else "",
        google_api_key=google_key.value if google_key else "",
        youtube_refresh_token=youtube_token.value if youtube_token else "",
        meta_user_access_token=meta_token.value if meta_token else "",
        facebook_page_id=fb_page_id.value if fb_page_id else "",
    )


@router.post("/settings/api_keys")
def update_api_keys(
    *,
    db: Session = Depends(deps.get_db),
    settings_in: ApiSettings,
    current_user: models.Usuario = Depends(deps.role_required(["admin_general"])),
):
    """
    Update API keys.
    """
    crud_settings.update_setting(db, key="openai_api_key", value=settings_in.openai_api_key)
    crud_settings.update_setting(db, key="google_api_key", value=settings_in.google_api_key)
    crud_settings.update_setting(db, key="youtube_refresh_token", value=settings_in.youtube_refresh_token)
    crud_settings.update_setting(db, key="meta_user_access_token", value=settings_in.meta_user_access_token)
    crud_settings.update_setting(db, key="facebook_page_id", value=settings_in.facebook_page_id)

    return {"status": "success", "message": "API keys updated successfully."}


@router.post("/settings/whatsapp")
def update_whatsapp_settings(
    *,
    db: Session = Depends(deps.get_db),
    settings_in: WhatsAppSettings,
    current_user: models.Usuario = Depends(deps.role_required(["admin_general"])),
):
    """
    Endpoint for the Admin General to update WhatsApp settings.
    These settings are stored in the new 'settings' table.
    """
    logger.info(f"Admin General ({current_user.nombre_usuario}) is updating WhatsApp settings.")

    crud_settings.update_setting(db, key="WHATSAPP_API_TOKEN", value=settings_in.api_token)
    crud_settings.update_setting(db, key="WHATSAPP_PHONE_NUMBER_ID", value=settings_in.phone_number_id)

    # The verify token is often static and defined by the developer,
    # but we could make it configurable as well if needed.
    # For now, we assume it's set in the .env file and configured once.

    logger.info("WhatsApp settings updated successfully in the database.")

    return {"status": "success", "message": "WhatsApp settings updated successfully."}