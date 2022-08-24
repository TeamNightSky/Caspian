import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=int(os.environ["PORT"]),
        reload=bool(os.environ.get("CASPIAN_DEBUG", "false").strip().lower() == "true"),
    )
