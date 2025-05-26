from datetime import timedelta

# Load the Whisper model (base)
model = whisper.load_model("base")


def transcribe_audio(file_path):
    try:
        # Transcribe audio file
        result = model.transcribe(file_path)

        # Extract segments
        segments = []
        for segment in result['segments']:
            start_time = str(timedelta(seconds=int(segment['start'])))
            text = segment['text'].strip()
            segments.append({
                "timestamp": start_time,
                "text": text
            })

        # Return the transcription result
        return segments
    except Exception as e:
        print(f"[ERROR] Transcription failed: {str(e)}")
        return None


# Test the function
if __name__ == "__main__":
    sample_audio = "sample.mp3"
    if os.path.exists(sample_audio):
        transcription = transcribe_audio(sample_audio)
        print(transcription)
    else:
        print("Sample audio file not found.")
