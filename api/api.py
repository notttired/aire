from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from starlette.middleware.cors import CORSMiddleware

from celery_config.tasks import scrape

from models.scrape_task import ScrapeRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    try:
        json_data = request.model_dump(mode="json")
        t_id = scrape.delay(json_data).id

        return {"status": "pending", "task_id": t_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results/{task_id}")
async def get_results(task_id: str):
    try:
        result = AsyncResult(task_id)

        if result.ready():
            if result.successful():
                return {"status": "success", "data": result.get()}
            else:
                return {"status": "failed", "error": str(result.info)}
        else:
            return {"status": "pending", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)