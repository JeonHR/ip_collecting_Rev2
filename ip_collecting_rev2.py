import socket
import os
from datetime import datetime
import pandas as pd

# IP 주소와 관련 정보를 딕셔너리로 반환하는 함수
def get_current_ip():
    hostname = socket.gethostname()
    
    # 시스템에 연결된 모든 IP 주소를 가져옴
    addr_info = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    
    # "10.86"으로 시작하는 IP 주소 필터링
    ipv4_address = next((info[4][0] for info in addr_info if info[4][0].startswith("10.86")), None)
    
    # 만약 조건에 맞는 IP 주소가 없을 경우 예외 처리
    if not ipv4_address:
        raise ValueError("No matching IP address found starting with '10.86'.")
    
    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 딕셔너리로 데이터 반환
    return {
        '컴퓨터 명': hostname,
        'IP 주소': ipv4_address,
        '수집 시간': execution_time
    }

# CSV 파일에 IP 주소와 실행 시간 업데이트
def update_drive_info_csv(data, output_file):
    # 새로운 데이터를 DataFrame으로 변환
    new_df = pd.DataFrame([data])

    # 파일이 있는지 확인
    if os.path.exists(output_file):
        try:
            # 기존 파일 읽기
            existing_df = pd.read_csv(output_file, encoding='utf-8-sig')

            # 동일한 컴퓨터 명의 기존 데이터 제거
            existing_df = existing_df[existing_df['컴퓨터 명'] != new_df['컴퓨터 명'].iloc[0]]
            
            # 새로운 데이터와 결합
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        except (pd.errors.EmptyDataError, KeyError):
            # 파일이 잘못된 경우 새로운 데이터를 사용
            updated_df = new_df
    else:
        # 파일이 없으면 새로운 데이터를 그대로 사용
        updated_df = new_df

    # CSV 파일에 저장 (헤더 포함, UTF-8 with BOM 인코딩)
    updated_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f'IP information updated in {output_file}')


if __name__ == "__main__":
    output_file = "Z:/Eagle/ENG_DATA/PTE DATA/HR/IP/IP.csv"

    try:
        # 새로운 IP 정보 가져오기
        new_data = get_current_ip()

        # CSV 파일 업데이트
        update_drive_info_csv(new_data, output_file)
    except ValueError as e:
        print(e)
