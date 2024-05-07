import cv2
import time
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_gdrive():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('drive', 'v3', credentials=creds)

def upload_file(service, filename, filepath, mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")

def capture_photo(service):
    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d_%H%M%S.jpg")
    save_path = filename

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return

    cv2.imwrite(save_path, frame)
    cap.release()

    upload_file(service, filename, save_path, 'image/jpeg')

if __name__ == "__main__":
    service = authenticate_gdrive()
    while True:
        capture_photo(service)
        time.sleep(60)