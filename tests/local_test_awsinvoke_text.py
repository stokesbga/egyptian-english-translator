import requests
import time

start = time.time()

url = 'http://127.0.0.1:7777/invocations'
body = {'route': 'translate_text', "arabic_text": "صياني يعني بتفقن في الصيني"}
resp = requests.post(url=url, params=body) 

end = time.time()
print('JSON:')
print(resp.json())
print(f'Request Processed in: {end-start} seconds')