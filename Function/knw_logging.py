import os
import sys

import datetime

import logging

import shutil
import traceback

gRetryCount = 5

def datetime_To_str(): # 날짜 정보 리스트로 반환
    now_datetime = datetime.datetime.now()
    return [now_datetime.strftime("%Y%m%d") , now_datetime.strftime("%Y/%m/%d/%H:%M")]

def make_Log_folder(): # Log 폴더가 없으면 폴더 생성
    if os.path.isdir("Log"):
        pass
    else:
        os.mkdir("Log")

sourcePath = f'Log/Log_{datetime_To_str()[0]}.log'
targetPath = os.path.dirname(sys.executable) + f'\\{datetime.date.today().strftime("%Y%m%d")}_작업로그.log'

def log_Error_write(*args): # 에러 로그 찍을때 사용할 함수
    if len(args) == 2:
        createLog = args[0]
        msg = args[1]
    else:
        createLog = False
        msg = args[0]

    # 로그 파일을 작성할 폴더 생성
    make_Log_folder()

    # 로깅 기본 설정
    logging.basicConfig(filename=sourcePath, level=logging.ERROR, encoding='utf-8')

    # 로그 기록
    logging.info(f'{datetime_To_str()[1]} : {msg}')
    print(msg)

    # 로깅 핸들러를 닫아 파일과의 연결 끊기
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()  # 핸들러 닫기

    # 로그 파일 복사
    if createLog:
        for retry in range(1, gRetryCount + 1):
            try:
                shutil.copy(sourcePath, targetPath)  # 파일 복사
                break
            except Exception as e:
                print(f"로그 파일 복사 실패, 재시도 {retry}/{gRetryCount}: {e}")
                if retry == gRetryCount:
                    print("최대 재시도 횟수 초과로 복사 실패.")
                    raise

def log_Info_write(*args):
    if len(args) == 2:
        createLog = args[0]
        msg = args[1]
    else:
        createLog = False
        msg = args[0]

    # 로그 파일을 작성할 폴더 생성
    make_Log_folder()

    # 로깅 기본 설정
    logging.basicConfig(filename=sourcePath, level=logging.INFO, encoding='utf-8')

    # 로그 기록
    logging.info(f'{datetime_To_str()[1]} : {msg}')
    print(msg)

    # 로깅 핸들러를 닫아 파일과의 연결 끊기
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()  # 핸들러 닫기

    # 로그 파일 복사
    if createLog:
        for retry in range(1, gRetryCount + 1):
            try:
                shutil.copy(sourcePath, targetPath)  # 파일 복사
                break
            except Exception as e:
                print(f"로그 파일 복사 실패, 재시도 {retry}/{gRetryCount}: {e}")
                if retry == gRetryCount:
                    print("최대 재시도 횟수 초과로 복사 실패.")
                    raise

def log_Warning_write(*args): # 워닝 로그 찍을때 사용할 함수
    if len(args) == 2:
        createLog = args[0]
        msg = args[1]
    else:
        createLog = False
        msg = args[0]

    # 로그 파일을 작성할 폴더 생성
    make_Log_folder()

    # 로깅 기본 설정
    logging.basicConfig(filename=sourcePath, level=logging.WARNING, encoding='utf-8')

    # 로그 기록
    logging.info(f'{datetime_To_str()[1]} : {msg}')
    print(msg)

    # 로깅 핸들러를 닫아 파일과의 연결 끊기
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()  # 핸들러 닫기

    # 로그 파일 복사
    if createLog:
        for retry in range(1, gRetryCount + 1):
            try:
                shutil.copy(sourcePath, targetPath)  # 파일 복사
                break
            except Exception as e:
                print(f"로그 파일 복사 실패, 재시도 {retry}/{gRetryCount}: {e}")
                if retry == gRetryCount:
                    print("최대 재시도 횟수 초과로 복사 실패.")
                    raise



