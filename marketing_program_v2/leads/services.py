import json
import os
import requests

key_ = os.environ["SECRET_KEY"]
id_ = os.environ["SECRET_ID"]
instance_ = os.environ["INSTANCE"]
base_url = 'mktorest.com'

client_id = '&client_id=53a15ef6-b27b-4a07-b5a4-596788ab3165'
client_secret = '&client_secret=10GLrCjCZrEC91Bf5iCJ6YbHXklVNDCv'
instance = '942-MYM-356'


def get_auth():
    identity_url = 'https://942-MYM-356.mktorest.com/identity/oauth/token?grant_type=client_credentials&&client_id=53a15ef6-b27b-4a07-b5a4-596788ab3165&client_secret=10GLrCjCZrEC91Bf5iCJ6YbHXklVNDCv'
    response = requests.request(identity_url)
    parsed_json = json.loads(response.text)
    print parsed_json
