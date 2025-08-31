import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import crud, schemas, models
from app.models.user import Role, RolesEnum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def seed_roles(db: Session):
    """Seeds the roles table from the RolesEnum."""
    logger.info("--- Seeding Roles ---")
    try:
        for role_enum in RolesEnum:
            role_in_db = db.query(Role).filter(Role.nombre == role_enum.value).first()
            if not role_in_db:
                db_role = Role(nombre=role_enum.value, descripcion=f"Rol para {role_enum.name}")
                db.add(db_role)
                logger.info(f"Creating role: {role_enum.value}")
        db.commit()
        logger.info("--- Roles seeded successfully ---")
    except Exception as e:
        logger.error(f"Could not seed roles: {e}")
        db.rollback()
        raise


def setup_parent_child_relationship():
    """
    Ensures a test parent and two test children exist and creates the
    relationship between them.
    """
    db: Session = SessionLocal()

    # First, ensure roles exist
    seed_roles(db)

    inquilino_id_for_test = 1
    logger.info("--- Setting up Parent-Child Test Data ---")

    # 1. Define users to create
    parent_username = "test_parent"
    child1_username = "test_child_01"
    child2_username = "test_child_02"

    users_data = [
        ("padre_acudiente", parent_username, "parent@test.com"),
        ("alumno", child1_username, "child1@test.com"),
        ("alumno", child2_username, "child2@test.com"),
    ]

    # 2. Create users if they don't exist
    for role, username, email in users_data:
        user = crud.user.get_user_by_username(db, username=username)
        if not user:
            user_in = schemas.UserCreate(
                email=email,
                password="password",
                nombre_usuario=username,
                nombre_completo=f"Test {username}",
                rol=role,
                inquilino_id=inquilino_id_for_test
            )
            try:
                crud.user.create_user(db=db, user=user_in)
                logger.info(f"User '{username}' with role '{role}' created.")
            except Exception as e:
                logger.error(f"Failed to create user '{username}': {e}")
                db.rollback()
        else:
            logger.info(f"User '{username}' already exists.")

    # 3. Fetch the users
    parent_user = crud.user.get_user_by_username(db, username=parent_username)
    child1_user = crud.user.get_user_by_username(db, username=child1_username)
    child2_user = crud.user.get_user_by_username(db, username=child2_username)

    if not all([parent_user, child1_user, child2_user]):
        logger.error("Could not fetch all required users. Aborting relationship setup.")
        db.close()
        return

    # 4. Create the relationship
    try:
        # Check if relationships already exist to avoid duplicates
        if child1_user not in parent_user.hijos:
            parent_user.hijos.append(child1_user)
            logger.info(f"Associating '{child1_username}' with '{parent_username}'.")
        else:
            logger.info(f"'{child1_username}' is already associated with '{parent_username}'.")

        if child2_user not in parent_user.hijos:
            parent_user.hijos.append(child2_user)
            logger.info(f"Associating '{child2_username}' with '{parent_username}'.")
        else:
            logger.info(f"'{child2_username}' is already associated with '{parent_username}'.")

        db.commit()
        logger.info("Successfully committed parent-child relationships.")

    except Exception as e:
        logger.error(f"An error occurred during relationship setup: {e}")
        db.rollback()

    finally:
        db.close()
        logger.info("--- Parent-Child Test Data Setup Finished ---")


if __name__ == "__main__":
    logger.info("Running parent-child relationship setup script directly.")
    setup_parent_child_relationship()
