import logging
import hashlib
from datetime import datetime, timezone
import urllib
import whisper
import os
import re
from pydub.utils import mediainfo

from decor.decorator import cost
from tools.tools import remove_file


def get_audio_format(filepath):
    info = mediainfo(filepath)
    return info['format_name']


@cost
def speech_to_text(audio_url:str) -> str :
    audio_file = hashlib.md5(audio_url.encode('utf-8')).hexdigest() + f"_{int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() * 1000)}"
    try :
        urllib.request.urlretrieve(audio_url, audio_file)
        model = whisper.load_model("base.en")
        logging.info(f"start task : {audio_file}")
        result = model.transcribe(audio_file)
        text = result["text"]
        logging.info(f"audio_url : {audio_url} ; text : {text}")
        if text :
            clear_text = re.sub(r'[^a-zA-Z0-9]', '', text)
            logging.info(f"audio_url : {audio_url} ; text : {text} ; clear_text : {clear_text}")
            return clear_text
        else :
            raise ValueError(f"speech_to_text fail.")
    except Exception as e :
        logging.error(f"audio_transcription err. audio_file : {audio_file} ; err : {e}")
        logging.exception(e)
        raise e
    finally :
        remove_file(audio_file)

