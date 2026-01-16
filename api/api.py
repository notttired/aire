from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from celery_config.tasks import scrape

from models.scrape_task import ScrapeRequest

app = FastAPI()


@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    try:
        json_data = request.model_dump(mode="json")
        t_id = scrape.delay(json_data).id
        res = AsyncResult(t_id).get(timeout=60)

        return {"status": "success", "data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
