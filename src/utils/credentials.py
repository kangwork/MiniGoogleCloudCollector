import os
import json
from google import oauth2

# credentials 가져오기
def get_credentials():

    # 방법 두 가지
    # A. 환경 변수 B. File path hardcoded(This is not recommended for security and reusability reasons.)

    # A-1. 터미널에서 환경 변수 설정하기
    # E.g. export GOOGLE_APPLICATION_CREDENTIALS='../local/mini-collector/key.json')

    # A-2. 변수에서 가져오기
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    # A-3. credentials 생성
    credentials = oauth2.service_account.Credentials.from_service_account_file(credentials_path)
    return credentials


    if credentials_path:
        # 1-1) Confirm the path
        while True:
            print(f'GOOGLE_APPLICATION_CREDENTIALS: {credentials_path}')
            # choice = input('Do you want to use this path? (y/n): ')

            # if choice == 'y':
            # A-3. credentials 생성
            try:
                # A-4. credentials 생성 (from_service_account_file -- path로 가져오는 것!)
                with open("../../local/mini-collector/key.json") as f:
                # B-2. json.load로 읽어들이기
                    credentials_info = json.load(f)  # json 파일을 dict로 변환

                # B-3. credentials 생성 (from_service_account_info -- dict로 가져오는 것!)
        
                credentials = oauth2.service_account.Credentials.from_service_account_info(credentials_info)
                print(credentials)
                return credentials
            except:
                print('Failed to get credentials.')
                exit(0)
            break
            # else:
            #     credentials_path = input('Enter the correct path(Orelse, press Enter to exit): ')
            #     if not credentials_path:
            #         exit(0)

    return credentials