import logging

import psycopg
from fastapi import FastAPI, HTTPException
from openai import APIError, APITimeoutError, RateLimitError
from pydantic import BaseModel, Field, field_validator

from app.hybrid_search import hybrid_search


logger = logging.getLogger(__name__)

app = FastAPI()


class SearchRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    limit: int = Field(default=20, ge=1, le=100, strict=True)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Question cannot contain only whitespace.")

        return cleaned


class SearchResult(BaseModel):
    chunk_id: int
    document_id: int
    title: str
    page: int
    url: str
    text: str
    rrf_score: float
    source_ranks: dict[str, int]


class SearchResponse(BaseModel):
    question: str
    count: int
    results: list[SearchResult]


@app.get("/")
def hello():
    return {"message": "Welcome"}


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    try:
        results = hybrid_search(
            request.question,
            limit=request.limit,
            candidate_limit=max(20, request.limit),
        )

    except APITimeoutError as exc:
        logger.exception("Embedding service timed out.")
        raise HTTPException(
            status_code=504,
            detail="The embedding service timed out. Try again later.",
        ) from exc

    except RateLimitError as exc:
        logger.exception("Embedding service request limit reached.")
        raise HTTPException(
            status_code=503,
            detail="The embedding service is temporarily unavailable.",
        ) from exc

    except APIError as exc:
        logger.exception("Embedding service request failed.")
        raise HTTPException(
            status_code=502,
            detail="The embedding service request failed.",
        ) from exc

    except psycopg.Error as exc:
        logger.exception("Database search failed.")
        raise HTTPException(
            status_code=503,
            detail="The database search service is unavailable.",
        ) from exc

    return SearchResponse(
        question=request.question,
        count=len(results),
        results=results,
    )