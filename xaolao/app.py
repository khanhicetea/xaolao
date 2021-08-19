from pydub.exceptions import PydubException
from starlette.responses import FileResponse, JSONResponse
from xaolao.utils import close_file_after_res, convert_url
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

CONTENT_TYPE_BY_FORMAT = {
    "wav": "audio/wav",
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg",
    "aac": "audio/aac",
    "adts": "audio/aac",
}

@app.get("/convert/url")
def convert(url: str, background_tasks: BackgroundTasks, from_format: str = "wav", to_format : str = "mp3"):
    try:
        sound_path = convert_url(url, from_format, to_format)
        background_tasks.add_task(close_file_after_res, sound_path)
    except PydubException:
        return JSONResponse({"status": "failed"}, status_code=500)
    return FileResponse(sound_path.name, media_type=CONTENT_TYPE_BY_FORMAT[to_format])
