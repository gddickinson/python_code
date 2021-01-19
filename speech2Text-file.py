#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 20:00:20 2020

@author: gdickinson
"""

from __future__ import division
import json
import speech_recognition as sr
from pydub import AudioSegment

r=sr.Recognizer()

key = {
  "type": "service_account",
  "project_id": "speech2text-266602",
  "private_key_id": "479deb23682035ebeba816953aaf2dd29b939855",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCdfrS8j4BNKytl\nnbrV+hNrQ/N3HMyOIWnq5GEThbOBcGeQ8e8Hwk57IXlFklmKWOLQM489st7V4ICQ\nNHvSgpS+1kW9NNtKCBFufp1V+BhfyuvuEysXngP/ocvKQtcolW8zdcoxBW0YKjcP\nUeDBH0zj4BHIEj6tXivzOjsPR6Duqa7lwgz9YUN/aTV0/rGLb7fIgSoAJTFAm7To\nadaceUVPRoNkgzZoESC9USYxOLVXI5SsCXucT9B3EZq988NSygVd/ayaPap5OJcD\nueqJTQJAyNczIey/+JHmw0RvlGMKREZcBcV+5W7N9N7aFYHPFElkVbgh/oTktwlN\nrJz4NUj9AgMBAAECggEAA/Z5M7lkoAxzBhaG6fVl4bAPAzM9TmI22QswCh62Go6q\nfHIp8ocIFH8OHxsEl7+OzXBOrV2/z5/bfEVlzDEu7vJTROR8lAtJ7P7QlKYubtKb\nRx1CW1DFhvwaNZei9El2R9Qx5zPcv9voEMGdpx5Tf/RWXjNfUltpPbB8ZfEGcprW\nRWmaOORZMcjNghKuZstMaTQgpoWW7uUD1zTl6MHMJWv9Dw3aLtN2REXja4CI3mXx\ndFQJa0Npl3twESY7tixRKgg4AHnpmM5fGDUWH6kH6d89TUNz3V7UONqCu8LGyg1r\nx+lZxI50vWr9kwUi7WTRTFbFTD3J1L+HBEFGv5gJoQKBgQDVCOGn10Vj9yq7ezbS\nnubEvf8K9/mj2vnEp8C4x7DPuuyPU/fIDfioVfssuZiJtBFwvRQ0ok+b70ndQGMv\n11+HIaApceJZEqAm+WxmwKOH57tkKCpu+8o2MuWAB6SfTN5MmC/63Egeukzs39fg\nRBCADVgOWytnnp+mMQNhnHk4yQKBgQC9QkWERsbwvmzZeJZGFqcwwDegQC0wfCa2\n7rtDJMeytlRKOCVl3QXTku+PX7mSuwIEiBv4/yZrCbdaqcNc7YRd4/iY8HtJhuQ2\ngm9OkuxMuIE8UXyEUGpYpaALJ+Vu2NgbZtKUx4c4zzwM/RR/xby7V+lh5WUIsrUn\nOI9OKcdclQKBgF4TXvsskGMVylQilFIsg8IMGS2x1hcq4zOZ1PyEiqshY8fjj79T\nlCRaW+IjT54325/Kj7qylq9I23iOL374ACJ/kefbd9ZX6EttyBYUKeMhTVpsdliu\nblzC2yBPv73tRxnR9xYz4tFW+hN8wisyQ4sY2XL1hdRrcxsD9/dKDyopAoGBAJwI\nGiX+8B8k77qvZz0rifVwU6wDnP3/LS/eTHcDyLw3A/EYrwR3H0maN3T915H4Kaaw\nzFcRjIvsu8S8dzuS+nEp9ReqFAq/ckDacofWK4jpCGtBRyYS4kppajQoVUh48FpP\nAEf25C3a9MhEknTxAjN2PAwgwpZUN3O5drRbT2itAoGBAMkJI8KV41lYeUS5Uaq/\n+yrnfxrzCgEdFJ8cSj5cBex7V7rFSSpubFB06CuZFRF57PWP5xiVThwYAa8sMVL5\nTe86WA0Dv79QEdetN0hChw90ll9V1v1oyrbFHb+Fvl1X0E/ty057YNOQgeeBIC9Q\nW7oqccZo2N+oiZGK/CtB+IEr\n-----END PRIVATE KEY-----\n",
  "client_email": "speech2text-439@speech2text-266602.iam.gserviceaccount.com",
  "client_id": "110707196601806828654",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/speech2text-439%40speech2text-266602.iam.gserviceaccount.com"
}

my_key = str(key)

#keyPath = r'/Users/gdickinson/Desktop/speech2Text-79eec229a0e0.json'


fileName = r'/Users/gdickinson/Desktop/Ari_Koufos.mp3'
fileName =r"C:\Users\George\Desktop\Ari_Koufos.mp3"
saveName = fileName.split('.')[0]+'.wav'
#saveName =r"C:\Users\George\Desktop\harvard.wav"
resultName = fileName.split('.')[0]+'.txt'

#wavFile = AudioSegment.from_mp3(fileName)
#wavFile.export(saveName, format="wav")
#print('wav file saved')


#with sr.AudioFile(saveName) as source:
#    # listen for the data (load audio to memory)
#    audio_data = r.record(source)
#    # recognize (convert from speech to text)
#    text = r.recognize_google(audio_data) #runs without API if no key given
#    print(text)

demo=sr.AudioFile(saveName)

with demo as source:
    #r.adjust_for_ambient_noise(source)
    audio=r.record(source,duration=120)
    #audio2=r.record(source,duration=120)

text = r.recognize_google_cloud(audio, credentials_json=my_key) 
#text = r.recognize_sphinx(audio)
#text2 = r.recognize_google(audio2) 

with open(resultName, "w") as text_file:
    text_file.write(text)

print(text) 
 
# =============================================================================
# # get audio from the microphone                                                                       
# r = sr.Recognizer()                                                                                   
# with sr.Microphone() as source:                                                                       
#     print("Speak:")                                                                                   
#     audio = r.listen(source)   
# 
# try:
#     print("You said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#     print("Could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results; {0}".format(e))
# =============================================================================
