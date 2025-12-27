import os
import json
import requests
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scope needed to upload photos
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.appendonly']

def get_service(account_name):
    creds = None
    token_file = f'token_{account_name}.pickle'
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

def upload_image(service, file_path):
    """Uploads a single file to Google Photos and returns the upload token."""
    filename = os.path.basename(file_path)
    
    # Get the binary data
    with open(file_path, 'rb') as f:
        data = f.read()

    # Get the access token for the request
    token = service._http.credentials.token
    if service._http.credentials.expired:
        service._http.credentials.refresh(Request())
        token = service._http.credentials.token

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': filename,
        'X-Goog-Upload-Protocol': 'raw',
    }

    print(f"⬆️ Uploading: {filename}...")
    response = requests.post(
        'https://photoslibrary.googleapis.com/v1/uploads',
        headers=headers,
        data=data
    )

    if response.status_code == 200:
        upload_token = response.content.decode('utf-8')
        # Finalize the upload in the library
        service.mediaItems().batchCreate(body={
            'newMediaItems': [{
                'description': 'Uploaded via Picasa Stock Tool',
                'simpleMediaItem': {'uploadToken': upload_token}
            }]
        }).execute()
        return True
    else:
        print(f"❌ Failed to upload {filename}: {response.text}")
        return False

def sync_folder(account_id, folder_path, metadata_file):
    """Checks metadata and uploads files that are not already in the cloud."""
    service = get_service(account_id)
    
    # Load already uploaded file names (if metadata file exists)
    existing_files = set()
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                existing_files.add(item.get('filename'))

    # Walk through the folder
    for root, _, files in os.walk(folder_path):
        for name in files:
            if name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.mp4', '.mov')):
                if name in existing_files:
                    # Skip already in cloud
                    continue
                
                success = upload_image(service, os.path.join(root, name))
                if success:
                    print(f"✅ Success: {name}")
                
if __name__ == '__main__':
    acc = input("Enter account label (user1/user2...): ")
    target_dir = input("Enter local folder path to sync: ")
    # Preferably get metadata first via 08 script
    meta = f'cloud_metadata_{acc}.json'
    
    sync_folder(acc, target_dir, meta)
