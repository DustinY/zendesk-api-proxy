import requests
import json

username = "upwork@adhocsupportllc.com"
password = "Fastapi123!!"

r = requests.post('http://localhost:8000/login', json={
    'username': username,
    'password': password
})

json_data = r.json()

status = json_data.get('status')
state_token = json_data.get('stateToken')
if status == 'MFA_REQUIRED':
    factors = json_data.get("_embedded").get('factors')
    factor_id = factors[0].get('id')
    
    code = input('Enter the TOTP code: ')
    verify_res = requests.post(f'http://localhost:8000/verify-mfa/{factor_id}', json={
        'passCode': code,
        'stateToken': state_token 
    })
    print(verify_res.status_code)
    print(json.dumps(verify_res.json(), indent=4))

# print(r.status_code)
# # print(r.content)
# print(json.dumps(r.json(), indent=4))