from app.api.healthcheck.controllers import healthcheck_router
from app.api.mem.controllers import mem_router

api_routers = [mem_router, healthcheck_router]
