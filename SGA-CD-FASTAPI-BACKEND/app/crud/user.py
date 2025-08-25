from sqlalchemy.orm import Session

# This import now works because `sga_cd_db` was installed as an editable package.
from models.user import Usuario
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_username(db: Session, username: str) -> Usuario | None:
    """
    Fetches a user from the database by their username.
    """
    return db.query(Usuario).filter(Usuario.nombre_usuario == username).first()

def create_user(db: Session, user: UserCreate) -> Usuario:
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(
        nombre_usuario=user.nombre_usuario,
        correo=user.email,
        password_hash=hashed_password,
        nombre_completo=user.nombre_completo,
        rol=user.rol,
        inquilino_id=user.inquilino_id,
        activo=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
