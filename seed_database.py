import sqlite3
import os

# --- Configuration ---
DB_FILE = os.path.join("Sarita-FASTAPI-BACKEND", "sga_cd.db")
ROLES = [
    "admin_general",
    "admin_empresa",
    "jefe_area",
    "profesional_area",
    "tecnico_area",
    "coordinador",
    "profesor",
    "alumno",
    "padre_acudiente",
    "jefe_almacen",
    "jefe_escenarios",
]

# --- Main Script ---
def seed_roles():
    """Connects to the database and inserts the predefined roles if they don't exist."""
    print(f"Connecting to database at: {DB_FILE}")
    if not os.path.exists(DB_FILE):
        print("Error: Database file not found. Please run the backend server once to create it.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Check if the roles table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='roles';")
        if cursor.fetchone() is None:
            # This is a fallback in case alembic didn't run.
            # The backend should create this table via its models.
            # If it's still missing, something is wrong with the model setup.
            print("Error: 'roles' table not found. Cannot seed roles.")
            print("Attempting to create it...")
            # This schema must match the SQLAlchemy model in Sarita-DB.git/models/user.py
            cursor.execute("""
            CREATE TABLE roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR NOT NULL,
                descripcion VARCHAR,
                CONSTRAINT uq_roles_nombre UNIQUE (nombre)
            )
            """)
            print("'roles' table created.")


        print("Seeding roles...")
        for role_name in ROLES:
            # Check if role already exists
            cursor.execute("SELECT id FROM roles WHERE nombre = ?", (role_name,))
            if cursor.fetchone():
                print(f"- Role '{role_name}' already exists. Skipping.")
            else:
                # Insert role
                cursor.execute("INSERT INTO roles (nombre, descripcion) VALUES (?, ?)", (role_name, f"Rol para {role_name}"))
                print(f"+ Role '{role_name}' added.")

        conn.commit()
        print("\nRoles seeding complete.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    seed_roles()
