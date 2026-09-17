from fastapi import FastAPI

app = FastAPI(
    title="NLP Mini System",
    description="NLP and Machine Learning Mini System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "NLP Mini System API is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }