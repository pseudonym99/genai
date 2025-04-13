from telegram import Update
from pydub import AudioSegment
import io
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter


def escape_markdown_v2(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


async def send_long_message(update: Update, long_text: str) -> None:
    """
    Sendet eine längere Nachricht in mehreren Teilen, wenn der Text zu lang ist.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=4096,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )
    
    text_splits = text_splitter.split_text(long_text)
    
    for text_split in text_splits:
        await update.message.reply_text(text_split)


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
