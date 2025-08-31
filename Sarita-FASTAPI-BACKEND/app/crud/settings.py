from sqlalchemy.orm import Session
from models import settings as models

def get_setting(db: Session, key: str) -> models.Setting | None:
    """
    Retrieves a setting from the database by its key.
    """
    return db.query(models.Setting).filter(models.Setting.key == key).first()

def update_setting(db: Session, key: str, value: str) -> models.Setting:
    """
    Creates or updates a setting in the database.
    """
    db_setting = get_setting(db, key)
    if db_setting:
        db_setting.value = value
    else:
        db_setting = models.Setting(key=key, value=value)
        db.add(db_setting)

    db.commit()
    db.refresh(db_setting)
    return db_setting
