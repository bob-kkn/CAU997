# 하위 프로세스 및 패키지 참조 --------------------------------------------------------------------------------------- #
import knw_license
import os
import sys
from os import environ
import tkinter as tk
from tkinter import messagebox as msgb
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from Common.log import Log
from Service.constants import Constants


# 전역변수 할당 ------------------------------------------------------------------------------------------------------ #
try:
    os.chdir(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

# 프로그램 실행 폴더
if getattr(sys, 'frozen', False):
    program_dir = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_dir = os.path.dirname(os.path.abspath(__file__))

constants = Constants()
logging = Log(program_dir)


# [메세지 박스] ------------------------------------------------------------------------------------------------------ #
def messageBox(messageType):
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)

    if messageType == 'emptyAccount':
        msgb.showwarning('info', '※ 계정이 입력되지 않았습니다.')
    elif messageType == 'start':
        root.after(2000, root.destroy)
        msgb.showwarning('info', '※ 작업을 시작합니다.')
    else:
        msgb.showerror('error', messageType)


# QMainWindow -------------------------------------------------------------------------------------------------------- #
# 작업을 별도의 쓰레드에서 처리하기 위한 클래스
class Worker(QThread):
    finished = pyqtSignal()

    def run(self):
        logging.log(f'▷ [{constants.PROCESS_NAME}] 시작')

        logging.log(f'   ▪ 입력받은 값 : {g_inputDate}')

        logging.log(f'□ [{constants.PROCESS_NAME}] 종료')


class Form(QMainWindow):
    # QMainWindow 설정 및 시작 --------------------------------------------------------------------------------------- #
    def __init__(self, parent=None):
        super().__init__()

        # 클래스 초기화
        self.ui = uic.loadUi("./Resource/main.ui", self)
        self.setFixedSize(350, 160)

        self.btn_start.clicked.connect(self.start)

    # [시작] 클릭 ---------------------------------------------------------------------------------------------------- #
    def start(self):
        global g_id, g_pw
        global g_inputDate
        
        # ui에서 입력받은 값 가져오기
        g_id = self.lineEdit_id.text().strip()
        g_pw = self.lineEdit_pw.text().strip()
        g_inputDate = self.lineEdit_Date.text().strip()

        # 계정이 입력되지 않았을 경우 예외처리 (메세지 박스)
        if ((g_id == '') | (g_pw == '')):
            messageBox('emptyAccount')
        else:
            messageBox('start')

            # ui창 숨기기
            self.hide()

            # 작업 실행
            self.worker = Worker()
            self.worker.finished.connect(self.on_finished)
            self.worker.start()

            # ui창 표시
            self.show()

    def on_finished(self):
        self.show()


# main --------------------------------------------------------------------------------------------------------------- #
def main():
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()