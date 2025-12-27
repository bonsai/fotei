import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scope for Google Drive (Uploading and managing files)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service(account_name):
    creds = None
    token_file = f'token_drive_{account_name}.pickle'
    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Error: 'credentials.json' not found.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def upload_screenshot_to_drive(service, file_path, folder_id=None):
    """Uploads a screenshot to a specific Google Drive folder."""
    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]
        
    media = MediaFileUpload(file_path, resumable=True)
    
    print(f"🚀 Uploading to Drive: {file_metadata['name']}...")
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print(f"✅ Created File ID: {file.get('id')}")
    return file.get('id')

def main():
    print("--- FOTEI: Screenshot Drive Sync ---")
    account_id = input("Enter account label (e.g., 'user1'): ")
    folder_path = input("Enter local screenshots folder path: ")
    drive_folder_id = input("Enter target Google Drive Folder ID (optional): ")
    
    service = get_drive_service(account_id)
    if not service: return

    for root, _, files in os.walk(folder_path):
        for name in files:
            if name.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_full_path = os.path.join(root, name)
                upload_screenshot_to_drive(service, file_full_path, drive_folder_id)

if __name__ == '__main__':
    main()
