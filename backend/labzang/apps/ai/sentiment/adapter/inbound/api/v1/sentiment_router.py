"""Hexagonal inbound API for sentiment service."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from labzang.apps.ai.sentiment.adapter.inbound.api.schemas import (
    BatchSentimentRequest,
    IngestRawRequest,
    SentimentRequest,
)
from labzang.apps.ai.sentiment.adapter.inbound.dependencies import (
    get_sentiment_command,
    get_sentiment_query,
)
from labzang.apps.ai.sentiment.application.ports.input import (
    SentimentCommand,
    SentimentQuery,
)

router = APIRouter(prefix="/sentiment", tags=["sentiment"])


@router.get("/")
async def sentiment_root():
    return {"service": "sentiment", "status": "running"}


@router.post("/analyze")
async def analyze_sentiment(
    request: SentimentRequest,
    query: SentimentQuery = Depends(get_sentiment_query),
):
    result = await query.analyze(request.text)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return JSONResponse(status_code=200, content={"success": True, "data": result})


@router.post("/batch")
async def analyze_batch_sentiment(
    request: BatchSentimentRequest,
    query: SentimentQuery = Depends(get_sentiment_query),
):
    results = await query.analyze_batch(request.texts)
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {
                "results": results,
                "total_count": len(results),
                "error_count": sum(1 for item in results if "error" in item),
            },
        },
    )


@router.post("/ingest/resources")
async def ingest_resources_data(
    command: SentimentCommand = Depends(get_sentiment_command),
):
    result = await command.ingest_resources_data()
    return JSONResponse(status_code=200, content={"success": True, "data": result})


@router.post("/ingest/raw")
async def ingest_raw_data(
    request: IngestRawRequest,
    command: SentimentCommand = Depends(get_sentiment_command),
):
    result = await command.ingest_reviews(request.rows)
    return JSONResponse(status_code=200, content={"success": True, "data": result})


@router.get("/health")
async def health(query: SentimentQuery = Depends(get_sentiment_query)):
    result = await query.health()
    code = 200 if result.get("status") == "healthy" else 503
    return JSONResponse(status_code=code, content={"success": code == 200, "data": result})


@router.get("/model/info")
async def model_info(query: SentimentQuery = Depends(get_sentiment_query)):
    result = await query.model_info()
    return JSONResponse(status_code=200, content={"success": True, "data": result})
