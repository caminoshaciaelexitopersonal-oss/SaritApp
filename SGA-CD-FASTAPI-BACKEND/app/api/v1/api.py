from fastapi import APIRouter
from .endpoints import (
    auth,
    alumnos,
    procesos,
    clases,
    inventory,
    gamification,
    billing,
    communication,
    curriculum,
    escenarios,
    eventos,
    inscripciones_asistencias,
    dropdowns,
    notificaciones,
    audit,
)

api_router = APIRouter()

# API Routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(alumnos.router, prefix="/alumnos", tags=["Alumnos"])
api_router.include_router(procesos.router, prefix="/procesos", tags=["Procesos de Formación"])
api_router.include_router(clases.router, prefix="/clases", tags=["Clases"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(gamification.router, prefix="/gamification", tags=["Gamification"])
api_router.include_router(billing.router, prefix="/billing", tags=["Billing"])
api_router.include_router(communication.router, prefix="/communication", tags=["Communication"])
api_router.include_router(curriculum.router, prefix="/curriculum", tags=["Curriculum"])
api_router.include_router(escenarios.router, prefix="/escenarios", tags=["Escenarios y Reservas"])
api_router.include_router(eventos.router, prefix="/eventos", tags=["Eventos"])
api_router.include_router(inscripciones_asistencias.router, prefix="/academic", tags=["Inscripciones y Asistencias"])
api_router.include_router(dropdowns.router, prefix="/dropdowns", tags=["Dropdown Management"])
api_router.include_router(notificaciones.router, prefix="/notificaciones", tags=["Notificaciones"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit Log"])
