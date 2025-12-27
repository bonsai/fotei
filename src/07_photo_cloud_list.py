import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def get_service(account_name):
    """Authenticator helper: manages separate tokens for multiple accounts."""
    creds = None
    token_file = f'token_{account_name}.pickle'
    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You need a credentials.json from Google Cloud Console
            if not os.path.exists('credentials.json'):
                print("Error: 'credentials.json' not found. Please download it from GCP Console.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

def list_media_items(service, output_file):
    """Fetches all media items and saves metadata to a JSON file."""
    items = []
    next_page_token = None
    
    print("🔍 Fetching media list from Google Photos...")
    
    while True:
        results = service.mediaItems().list(
            pageSize=100, 
            pageToken=next_page_token
        ).execute()
        
        items.extend(results.get('mediaItems', []))
        next_page_token = results.get('nextPageToken')
        
        print(f"✅ Loaded {len(items)} items...")
        
        if not next_page_token:
            break

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    
    print(f"✨ Finished! Metadata for {len(items)} items saved to {output_file}")

if __name__ == '__main__':
    # Account identifier (e.g., 'personal', 'work')
    # This keeps tokens separate for multi-account management
    account_id = input("Enter an account label (e.g., 'user1'): ")
    
    service = get_service(account_id)
    if service:
        list_media_items(service, f'cloud_metadata_{account_id}.json')
