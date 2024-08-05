from app.api.authentication.controllers import authentication_router
from app.api.healthcheck.controllers import healthcheck_router
from app.api.mem.controllers import mem_router
from app.api.users.controllers import user_router

api_routers = [authentication_router, user_router, mem_router, healthcheck_router]
