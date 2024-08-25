import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import urllib
import hashlib
from datetime import datetime, timezone
from PIL import Image
import re

from tools.tools import remove_file



class Moondream2ImageCaptcha:
    
    def __init__(self) -> None:
        model_id = "ayoubkirouane/moondream2-image-captcha"
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id , trust_remote_code=True)
        
    def solve_captcha(self, image_url:str) -> str :
        image_file = hashlib.md5(image_url.encode('utf-8')).hexdigest() + f"_{int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() * 1000)}"
        try :
            urllib.request.urlretrieve(image_url, image_file)
            image = Image.open(image_file)
            enc_image = self.model.encode_image(image)
            prompt = """Returns the 6-digit verification code in the image.
            Returns in json format: {"captcha":XXXXXX}"""
            text = self.model.answer_question(enc_image, prompt, self.tokenizer)
            if text :
                clear_text = re.sub(r'[^a-zA-Z0-9]', '', text)
                logging.info(f"image_url : {image_url} ; text : {text} ; clear_text : {clear_text}")
                return clear_text
            else :
                raise ValueError(f"Moondream2ImageCaptcha solve_captcha fail.")
        except Exception as e :
            logging.error(f"Moondream2ImageCaptcha solve_captcha err. image_file : {image_file} ; err : {e}")
            logging.exception(e)
            raise e
        finally :
            remove_file(image_file)