from functools import lru_cache

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_NAME = "BAAI/bge-reranker-v2-m3"
MAX_LENGTH = 1024


@lru_cache(maxsize=1)
def load_reranker():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        use_safetensors=True,
    )
    model.to("cpu")
    model.eval()

    return tokenizer, model


def rerank(question, candidates, limit=5):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a nonempty string.")

    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("Limit must be a positive integer.")

    for candidate in candidates:
        text = candidate.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Each candidate must contain nonempty text.")

    if not candidates:
        return []

    tokenizer, model = load_reranker()
    ranked = []

    for candidate in candidates:
        text = candidate["text"]

        full_tokens = tokenizer(
            question,
            text,
            truncation=False,
        )["input_ids"]

        inputs = tokenizer(
            question,
            text,
            padding=False,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )

        with torch.inference_mode():
            logit = model(**inputs).logits.reshape(-1)[0]

            if not torch.isfinite(logit).item():
                raise RuntimeError("Reranker produced a non-finite score.")

            score = torch.sigmoid(logit).item()

        result = candidate.copy()
        result["rerank_score"] = score
        result["rerank_truncated"] = len(full_tokens) > MAX_LENGTH
        ranked.append(result)

    ranked.sort(key=lambda result: result["rerank_score"], reverse=True)

    return ranked[:limit]