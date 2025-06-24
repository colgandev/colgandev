"""
Simple api endpoints around my desktop machine that allow me to access the desktop system from Android and iOS via my Tailscale tailnet, and my custom Chrome plugin locally.
"""

import subprocess

from fastapi import FastAPI, Request, Response

app = FastAPI()


@app.post("/clipboard")
async def set_clipboard(request: Request):
    # Get the raw body as bytes and decode to string
    text = (await request.body()).decode("utf-8")

    subprocess.run(["xclip"], input=text.encode())
    return Response("success")
