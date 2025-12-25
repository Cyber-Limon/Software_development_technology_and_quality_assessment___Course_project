import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.company_api import company_api
from routes.room_api import room_api
from routes.user_api import user_api
from routes.sensor_api import sensor_api
from routes.limitation_api import limitation_api
from routes.monitoring_api import monitoring_api



app = FastAPI(
    title="Система контроля и управления датчиками",
    description="REST API для системы мониторинга помещений",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(company_api)
app.include_router(room_api)
app.include_router(user_api)
app.include_router(sensor_api)
app.include_router(limitation_api)
app.include_router(monitoring_api)

@app.get("/")
def read_root():
    return {
        "message": "Система контроля и управления датчиками",
        "docs": "/docs",
        "api": "/api"
    }


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
