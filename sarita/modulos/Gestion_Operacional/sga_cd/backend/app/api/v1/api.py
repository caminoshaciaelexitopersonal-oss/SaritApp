from fastapi import APIRouter
from .endpoints import (
    auth,
    admin,
    agent,
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
    tenancy,
    profesor,   # profesor ya estaba en main y en la feature
    jefe_area,  # agregado desde feat/implement-roles-and-agent-ui
    webhooks,
    admin_general,
    sales_agent,  # agregado desde feature/implement-role-views
    padre,
    video_distribution,
    meta,
    google,
    brand,
    calendar,
)

api_router = APIRouter()

# API Routers
api_router.include_router(sales_agent.router, prefix="/sales_agent", tags=["Sales Agent"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
api_router.include_router(admin_general.router, prefix="/admin_general", tags=["Admin General"])
api_router.include_router(brand.router, prefix="/brand-profile", tags=["Brand Profile"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(meta.router, prefix="/auth", tags=["Meta Authentication"]) # Using /auth prefix
api_router.include_router(google.router, prefix="/auth", tags=["Google Authentication"])
api_router.include_router(tenancy.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(padre.router, prefix="/padre", tags=["Padre Acudiente"])
api_router.include_router(profesor.router, prefix="/profesor", tags=["Profesor"])
api_router.include_router(jefe_area.router, prefix="/jefe_area", tags=["Jefe de Área"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(agent.router, prefix="/agent", tags=["AI Agent"])
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
api_router.include_router(video_distribution.router, prefix="/video_distribution", tags=["Video Distribution"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit Log"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["Content Calendar"])