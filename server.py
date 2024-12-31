import uvicorn 
from app.main import app


uvicorn.run("app.main:app",
            host="0.0.0.0",
            port=5000,
            # reload=True,
            log_level="info"
)