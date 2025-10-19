from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from scipy.io.wavfile import write
from starlette.middleware.cors import CORSMiddleware
import io
import uvicorn
import app

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class TtsRequest(BaseModel):
    model_name: str
    speed: int
    tts_text: str
    tts_voice: str
    f0_up_key: int
    f0_method: str
    index_rate: int
    protect: int


@api.get("/")
async def root():
    return {"message": "Hello World"}


@api.post("/tts")
async def tts(request: TtsRequest):
    print(request)
    (info, edge_output_filename, tts_output) = await app.tts(
        request.model_name,
        request.speed,
        request.tts_text,
        request.tts_voice,
        request.f0_up_key,
        request. f0_method,
        request.index_rate,
        request.protect
    )

    if tts_output is not None:
        # data information
        print("Sampling rate:", tts_output[0])
        print("Frame num:", tts_output[1].shape[0])
        print("Sec:", tts_output[1].shape[0] / tts_output[0])
        print("Numpy dtype:", tts_output[1].dtype)

        # write wav
        wav_data = io.BytesIO()
        write(wav_data, rate=tts_output[0], data=tts_output[1])
        wav_data.seek(0)  # ストリームの先頭に戻す
        # write("tts_output.wav", rate=tts_output[0], data=tts_output[1])  # ファイルとしても書き出し

        return StreamingResponse(wav_data, media_type="audio/wav", headers={"Content-Disposition": "inline; filename=data.wav"})
    else:
        raise HTTPException(status_code=500, detail="音声生成に失敗しました。")

if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=8001, log_level="debug")
