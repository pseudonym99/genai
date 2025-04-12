from pydub import AudioSegment
import io


def convert_ogg_bytes_to_wav_bytes(ogg_bytes):
    """Konvertiert OGG-Bytes (OPUS) in WAV-Bytes."""
    try:
        audio = AudioSegment.from_ogg(io.BytesIO(ogg_bytes))
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)  # Zurück zum Anfang des Buffers
        return wav_buffer.getvalue()
    except Exception as e:
        raise ValueError(f"Fehler bei der Konvertierung der OGG-Bytes: {e}")