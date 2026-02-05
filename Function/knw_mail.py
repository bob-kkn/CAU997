# 패키지 Install ----------------------------------------------------------------------------------------------------- #
package_list = [
    'cryptography==41.0.1'
]

import subprocess

try:
    subprocess.run(['pip', 'install'] + package_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except:
    print('※ 패키지 설치 PASS')

# 패키지 Import ------------------------------------------------------------------------------------------------------ #
from cryptography.fernet import Fernet

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email import encoders

import os
from os import environ

import traceback

try:
    os.chdir(sys._MEIPASS)
except:
    os.chdir(os.getcwd())


# 계정 복호화 (dev.knwrpa1) ----------------------------------------------------------------------------- #
encrypt_key = b'EQtrRQcHI1JzBCRXYGLib8F2mE-E1dCktfREZMNzYkE='
encrypt_id = 'gAAAAABkq8GiPSJuV7gp0l60ttieUcpf5Dj14CP1lchojtijgX0zDJdmixHr0oY5BRMPwFIoJJOUHGYZHpF7oCLGRdrK8R4mr-WEIBX49HicDyTf2s2nw5Q='
encrypt_pw = 'gAAAAABkq8GjEdJ_Wz7j7tBvT2UqUcSXn-HiUgB5fH4On4GOHcjvN2Czt6oR3P-USbwwP70-L0Ll3GcgyN0ih0sMdc7v77d-qG--L9pPVHAcnD8ZQXOCIjQ='

cipher_suite = Fernet(encrypt_key)
smtpId = cipher_suite.decrypt(encrypt_id.encode()).decode()
smtpPw = cipher_suite.decrypt(encrypt_pw.encode()).decode()

# 메일 보내기 -------------------------------------------------------------------------------------------------------- #
def sendMail(*args):
    """
    [메일 보내기]

    :Args
        - (필수) mailSubject : 메일 제목
        - (선택) mailBody : 메일 본문
        - (선택) mailTo : 수신자
        - (선택) mailAttachment : 첨부파일

    :Example
        - Mail.sendMail([mailSubject, mailBody, mailTo, mailAttachments])
        - Mail.sendMail(mailSubject, mailBody, mailTo, mailAttachments)
    """
    try:
        # 입력받은 인수 할당 ----------------------------------------------------------------------------------------- #
        gap = ''
        
        mailSubject = ''
        mailTo = ''
        mailCc = ''
        mailBcc = ''
        mailBody = ''
        mailAttachments = ''
        html_content = ''
        
        if type(args[0]) == list:
            for idx, row in enumerate(args[0]):
                # 갭
                if (idx == 0) and (row.strip() == ''):
                    gap = row + '   '

                # 메일 수신자
                elif ('@knworks.co.kr' in str(row)) and ('수신' in str(row)):
                    mailTo = str(row).replace('[', '').replace(']', '').replace('\'', '').replace('수신, ','')
                    # 메일 비밀 참조자
                elif ('@knworks.co.kr' in str(row)) and ('비밀참조' in str(row)):
                    mailBcc = str(row).replace('[', '').replace(']', '').replace('\'', '').replace('비밀참조, ', '')
                # 메일 참조자
                elif ('@knworks.co.kr' in str(row)) and ('참조' in str(row)):
                    mailCc = str(row).replace('[', '').replace(']', '').replace('\'', '').replace('참조, ','')

                # 메일 첨부파일
                elif 'C:\\' in str(row).upper() or '.LOG' in str(row).upper():
                    mailAttachments = row
                # 메일 본문
                elif (idx != 0) and (idx != 1) and (not '<html>' in row):
                    mailBody = row
                # html 태그
                elif '<html>' in row:
                    html_content = row
                # 메일 제목
                else:
                    mailSubject = row
        else:
            for idx, row in enumerate(args):
                # 갭
                if (idx == 0) and (row.strip() == ''):
                    gap = row + '   '

                # 메일 수신자
                elif ('@knworks.co.kr' in str(row)) and ('수신' in str(row)):
                    mailTo = str(row).replace('[', '').replace(']', '').replace('\'', '').replace('수신, ','')
                # 메일 비밀 참조자
                elif ('@knworks.co.kr' in str(row)) and ('비밀참조' in str(row)):
                    mailBcc = str(row).replace('[', '').replace(']', '').replace('\'', '').replace('비밀참조, ', '')
                # 메일 참조자
                elif ('@knworks.co.kr' in str(row)) and ('참조' in str(row)):
                    mailCc = str(row).replace('[', '').replace(']', '').replace('\'', '').replace('참조, ','')

                # 메일 첨부파일
                elif 'C:\\' in str(row).upper() or '.LOG' in str(row).upper():
                    mailAttachments = row
                # 메일 본문
                elif (idx != 0) and (idx != 1) and (not '<html>' in row):
                    mailBody = row
                # html 태그
                elif '<html>' in row:
                    html_content = row
                # 메일 제목
                else:
                    mailSubject = row

        print(f'{gap}▷ [sendMail] 시작')

        # 1. SMTP 서버 연결
        smtp = smtplib.SMTP_SSL('smtp.kakaowork.com', 465)

        # 2. SMTP 서버에 로그인
        smtp.login(smtpId, smtpPw)

        # 3. MIME 형태의 이메일 메세지 작성
        message = MIMEMultipart()

        message['Subject'] = mailSubject
        message['From'] = smtpId

        if html_content != '':
            message.attach(MIMEText(html_content, 'html'))
        
        # 수신자가 있을경우 누적
        if mailTo != '':
            message['To'] = mailTo

        # 참조자가 있을경우 누적
        if mailCc != '':
            message['Cc'] = mailCc

        # 비밀 참조자가 있을경우 누적
        if mailBcc != '':
            message['Bcc'] = mailBcc
        else:
            message['Bcc'] = smtpId

        # 수신, 참조, 비밀참조가 다 비어있을 경우
        if (mailTo == '') and (mailCc == '') and (mailBcc == '') and (message['Bcc'] != smtpId):
            message['To'] = smtpId
        
        # 본문이 있을경우 누적
        if mailBody != '':
            message.attach(MIMEText(mailBody, 'html'))

        # 첨부파일이 있을경우 누적
        if mailAttachments != '':
            for mailAttachments_idx, mailAttachments_row in enumerate(mailAttachments):

                print(f'{gap}   - 첨부파일 : ' + mailAttachments_row)

                attachment = MIMEBase('application', 'octet-stream')
                with open(mailAttachments_row, 'rb') as file:
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                file_name = os.path.basename(mailAttachments_row)
                file_name_encoded = Header(file_name, 'utf-8').encode()

                attachment.add_header('Content-Disposition', f'attachment; filename={file_name_encoded}')
                message.attach(attachment)

        # 4. 서버로 메일 보내기
        smtp.send_message(message)

        # 5. 메일을 보내면 서버와의 연결 끊기
        smtp.quit()
        print(f'{gap}   • 제목 : {mailSubject}')

        if mailTo != '':
            print(f'{gap}   • 수신 : {mailTo}')

        if mailCc != '':
            print(f'{gap}   • 참조 : {mailCc}')

        if mailBcc != '':
            print(f'{gap}   • 비밀 참조 : {mailBcc}')

        print(f'{gap}□ [sendMail] 종료')
    except Exception as e:
        raise Exception(f'{gap}   ※ [sendMail] 오류 : ' + str(e))