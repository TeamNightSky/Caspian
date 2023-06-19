import os

import uvicorn

from api import DEBUG


if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=int(os.environ["PORT"]),
        reload=DEBUG,
    )
