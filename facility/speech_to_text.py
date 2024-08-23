import logging
import hashlib
from datetime import datetime, timezone
import urllib
import whisper
import os

from decor.decorator import cost

def __remove_file(fn) -> None:
    if fn and os.path.exists(fn):
        os.remove(fn)

@cost
def speech_to_text(audio_url:str) -> str :
    audio_file = hashlib.md5(audio_url.encode('utf-8')).hexdigest() + f"_{int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() * 1000)}"
    urllib.request.urlretrieve(audio_url, audio_file)
    try :
        model = whisper.load_model("tiny.en")
        logging.info(f"start task : {audio_file}")
        result = model.transcribe(audio_file)
        text = result["text"]
        logging.info(f"audio_url : {audio_url} ; text : {text}")
        if text :
            clear_text = text.replace(', ','').strip().strip('.')
            logging.info(f"audio_url : {audio_url} ; text : {text} ; clear_text : {clear_text}")
            return clear_text
        else :
            raise ValueError(f"")
    except Exception as e :
        logging.error(f"audio_transcription err. audio_file : {audio_file} ; err : {e}")
        logging.exception(e)
    finally :
        __remove_file(audio_file)
