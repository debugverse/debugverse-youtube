from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama
import whisper
import uuid
from pathlib import Path
from openai import OpenAI
from langchain_core.messages import HumanMessage


####################
# Code by Debugverse
# https://www.youtube.com/@DebugVerseTutorials
####################

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whisper_model = whisper.load_model("small")
llm = ChatOllama(model="llama3.1:latest", temperature=1)
client = OpenAI()


def get_llm_response(text):
    messages = [
        HumanMessage(content=text)
    ]
    response = llm.invoke(messages)
    return response.content


def generate_tts_file(text):
    file_name = f"speech_{str(uuid.uuid4())}.mp3"
    speech_file_path = Path.cwd() / "responses" / file_name
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=text
        )
        response.write_to_file(speech_file_path)
        return speech_file_path
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None


# Endpoint to handle audio upload and processing
@app.post("/process_audio")
async def process_audio(audio: UploadFile = File(...)):
    # Save uploaded audio file
    file_path = Path(f"{uuid.uuid4()}.mp3")
    with open(file_path, "wb") as f:
        f.write(audio.file.read())

    # Transcribe audio with Whisper
    result = whisper_model.transcribe(str(file_path))
    user_text = result["text"]

    print(f"User text: {user_text}")
    # Generate LLM response
    response_text = get_llm_response(user_text)

    # Generate TTS audio
    tts_file_path = generate_tts_file(response_text)
    if tts_file_path:
        return FileResponse(tts_file_path, media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=500, detail="TTS generation failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
