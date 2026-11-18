from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

MODEL = "text-embedding-3-small"
DIMENSIONS = 1536


def embed_text(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a nonempty string.")

    response = client.embeddings.create(
        model=MODEL,
        input=text,
        dimensions=DIMENSIONS,
        encoding_format="float",
    )

    embedding = response.data[0].embedding

    if len(embedding) != DIMENSIONS:
        raise ValueError("Unexpected embedding dimensions.")

    return embedding