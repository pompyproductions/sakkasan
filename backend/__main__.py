import uvicorn

# uvicorn.run tells the uvicorn server to run our `app`.
# "main:app"  -> looks for the `app` variable in the `main.py` file (or __main__.py in this case)
# reload=True -> hot reloading
uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)