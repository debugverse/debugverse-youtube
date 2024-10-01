
import mlx_whisper

text = mlx_whisper.transcribe(
    "voice.mp3",
    path_or_hf_repo="mlx-community/whisper-turbo")["text"]


print(text)