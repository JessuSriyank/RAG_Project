from google_auth_oauthlib.flow import InstalledAppFlow

# Path to your credentials.json file
credentials_path = '/home/dtel/Desktop/Grog/client.json'

# Path to save the token.json file
token_path = '/home/dtel/Desktop/Grog/token.json'

# OAuth2 flow
flow = InstalledAppFlow.from_client_secrets_file(
    credentials_path, 
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Run the flow to authorize and save the credentials
creds = flow.run_local_server(port=6060, access_type='offline', prompt='consent')

# Save the credentials to token.json
with open(token_path, 'w') as token:
    token.write(creds.to_json())
