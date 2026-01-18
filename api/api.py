from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from celery_config.tasks import scrape

from models.scrape_task import ScrapeRequest

app = FastAPI()

# Add CORS middleware BEFORE any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.options("/scrape")
async def scrape_options():
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
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