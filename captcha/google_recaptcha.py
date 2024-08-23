import logging
import os,urllib,random,pydub,speech_recognition,time
from DrissionPage.common import Keys
from DrissionPage import ChromiumPage
from datetime import datetime, timezone


class RecaptchaSolver:
    def __init__(self, driver:ChromiumPage):
        self.driver = driver
    
    
    def _gain_audio_file_name(self) -> str :
        file_name = f"{int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() * 1000)}_{random.randrange(1,1000)}"
        return file_name
    
    
    def _delete_file(self, fn:str) -> None :
        if fn and os.path.exists(fn):
            os.remove(fn)
    
    
    def solveCaptcha(self) -> bool:
        file_name = self._gain_audio_file_name()
        path_to_mp3 = f"./{file_name}.mp3"
        path_to_wav = f"./{file_name}.wav"
        try :
            iframe_inner = self.driver("@title=reCAPTCHA")
            time.sleep(0.1)
            
            # Click on the recaptcha
            iframe_inner('.rc-anchor-content',timeout=1).click()
            self.driver.wait.ele_displayed("xpath://iframe[contains(@title, 'recaptcha')]",timeout=3)

            # Sometimes just clicking on the recaptcha is enough to solve it
            if self.isSolved():
                return
            
            # Get the new iframe
            iframe = self.driver("xpath://iframe[contains(@title, 'recaptcha')]")

            # Click on the audio button
            iframe('#recaptcha-audio-button',timeout=1).click()
            time.sleep(0.5)
            
            # Get the audio source
            src = iframe('#audio-source').attrs['src']
            
            
            urllib.request.urlretrieve(src, path_to_mp3)

            # Convert mp3 to wav
            sound = pydub.AudioSegment.from_mp3(path_to_mp3)
            sound.export(path_to_wav, format="wav")
            sample_audio = speech_recognition.AudioFile(path_to_wav)
            r = speech_recognition.Recognizer()
            with sample_audio as source:
                audio = r.record(source)
            
            # Recognize the audio
            key = r.recognize_google(audio)
            
            # Input the key
            iframe('#audio-response').input(key.lower())
            time.sleep(0.3)
            
            # Submit the key
            iframe('#audio-response').input(Keys.ENTER)
            time.sleep(1)

            # Check if the captcha is solved
            return self.isSolved()
        except Exception as e :
            logging.error(f"solve reCaptcha fail. e : {e}")
        finally :
            self._delete_file(path_to_mp3)
            self._delete_file(path_to_wav)

    def isSolved(self):
        try:
            return "style" in self.driver("@title=reCAPTCHA").ele(".recaptcha-checkbox-checkmark",timeout=1).attrs
        except:
            return False
