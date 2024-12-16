import requests
import time

start = time.time()

url = 'http://127.0.0.1:7777/translate-audio'
files = [('audio_file', open('app/demo.wav', 'rb'))]
resp = requests.post(url=url, files=files) 

end = time.time()
print(resp.json())
print(f'Request Processed in: {end-start} seconds')