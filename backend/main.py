import config.fastapiconfig as apicfg
import config.db_connection as dbconn
import signal
import os
import sys
import subprocess
from fastapi import FastAPI
import routes.usermanager as usermanager
import routes.recipemanager as recipemanager
import routes.favoritemanager as favoritemanager


app = apicfg.create_configured_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(usermanager.router)
app.include_router(recipemanager.router)
app.include_router(favoritemanager.router)

if __name__ == "__main__":
    subprocess.run(
        [sys.executable, "-m", "fastapi", "dev", "main.py", "--port", "3000"]
    )
    # os.kill(os.getpid(),signal.SIGINT)
