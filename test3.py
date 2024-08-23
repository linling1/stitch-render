import os,urllib,random,pydub,speech_recognition,time
from pydub.utils import mediainfo

# url = "https://state.sor.gbi.ga.gov/sort_public/LanapCaptcha.aspx?get=sound&c=captcha_ctl00_contentplaceholder1_botdetectcaptcha&t=7a00fa4e70f3445a8d0fa9310472670f&s=eoxzrm5q50m421bwqpyqzhqx&d=1724284442112"

file_name = '/Users/linling/Desktop/aaa.wav'
# urllib.request.urlretrieve(url, file_name)




def get_audio_format(filepath):
    info = mediainfo(filepath)
    return info['format_name']

# Example usage
audio_format = get_audio_format(file_name)
print(f'The audio format is: {audio_format}')

sample_audio = speech_recognition.AudioFile(file_name)
r = speech_recognition.Recognizer()
with sample_audio as source:
    audio = r.record(source)
    key = r.recognize_google(audio)
    print(key)