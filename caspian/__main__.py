import os
import uvicorn


if __name__ == "__main__":
    uvicorn.run("caspian.app:app", host="0.0.0.0", port=int(os.environ["PORT"]))
