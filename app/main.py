import asyncio

import uvicorn
from fastapi import FastAPI

from app.api.api import api_routers
from app.core.helpers.creation_helper import CreationHelper

app = FastAPI()

for api_router in api_routers:
    app.include_router(api_router, prefix="/api")


async def main():
    CreationHelper.create_image_bucket()
    await CreationHelper.create_base_admin()
    uvicorn.run(app="main:app", host='0.0.0.0', port=3000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
