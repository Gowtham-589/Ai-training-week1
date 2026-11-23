import os
import hashlib
import hmac
import os
import requests
from pathlib import Path
from typing import Any, Dict, List
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY =os.getenv("API_KEY")
WEBHOOK_SECRET=os.getenv("WEBHOOK_SECRET")

print("API key loaded:",bool(API_KEY))
print("webhook secret loaded:",bool(WEBHOOK_SECRET))

session =requests.session()

retry_strategy =Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500,502,503,504],
     allowed_methods=["GET"]
)

adapter =HTTPAdapter(max_retries=retry_strategy)
session.mount("https://",adapter)
print("session cretaed successfully")

url="https://jsonplaceholder.typicode.com/users"

response=session.get(url,timeout=10)
response.raise_for_status()

users=response.json()
print("\nFIRST 5 USERS")

for user in users[:5]:
    print(
        f"{user.get('id','not available')}-"
        f"{user.get('name','not available')}-"
        f"{user.get('email','not available')}-"
    )

first_user =users[0] if users else {}

address= first_user .get("address",{})
geo = address.get("geo",{})

company =first_user.get("company",{}) 
city=address.get("city","Not available")
latitude =geo.get("lat","Not available")
Zip_code =address.get("Zip_code","Not available")
company_name =company.get("name","Not available")

print("/nFIRST USER DETAILS")
print("city:",city)
print("latitude:",latitude)
print("zip:",Zip_code)
print("company:",company_name)

def verify_signature(payload,signature,secret):
    expected_signature =hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha3_256
    ).hexdigest()
    return  hmac.compare_digest(expected_signature,signature)

payload = b'{"event":"test"}'
secret = WEBHOOK_SECRET or ""
expected_signature = hmac.new(
    secret.encode("utf-8"),
    payload,
    hashlib.sha3_256
).hexdigest()
valid = verify_signature(payload, expected_signature, secret)

tampered =verify_signature(payload,"wrong_signature",secret)
wrong=verify_signature(payload,expected_signature,"incorrect_secret")

print("\nSIGNATURE VERIFICATION")
print(
    f"valid:{valid}|"
    f"Tampered:{tampered}|"
    f"Wrong secret:{wrong}"
)
