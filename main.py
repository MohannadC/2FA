import smtplib
import sys
import sqlite3
from scripts import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        self.counter = 5
        super().__init__()
        uic.loadUi('main.ui', self)
        self.show_main_win()

        self.submit_code_bb.clicked.connect(self.act_code)
        self.submit_reg_bb.clicked.connect(self.act_reg)
        self.submit_log_bb.clicked.connect(self.act_log)
        self.register_bb.clicked.connect(self.show_reg_win)

        self.back_bb.clicked.connect(self.show_main_win)
        self.login_bb.clicked.connect(self.show_log_win)

    def show_main_win(self):
        self.submit_code_bb.hide()
        self.submit_reg_bb.hide()
        self.submit_log_bb.hide()
        self.ll.hide()
        self.password_edit.hide()
        self.email_edit.hide()
        self.back_bb.hide()
        self.register_bb.show()
        self.login_bb.show()

    def show_reg_win(self):
        self.password_edit.show()
        self.email_edit.show()
        self.ll.show()
        self.submit_code_bb.hide()
        self.submit_reg_bb.show()
        self.submit_log_bb.hide()
        self.back_bb.show()
        self.register_bb.hide()
        self.login_bb.hide()
        self.ll.setText('Enter your email and password')

    def show_log_win(self):
        self.password_edit.show()
        self.email_edit.show()
        self.ll.show()
        self.submit_code_bb.hide()
        self.submit_reg_bb.hide()
        self.submit_log_bb.show()
        self.back_bb.show()
        self.register_bb.hide()
        self.login_bb.hide()
        self.ll.setText('Enter your email and password')

    def show_code_win(self):
        self.password_edit.show()
        self.email_edit.hide()
        self.ll.show()
        self.submit_code_bb.show()
        self.submit_reg_bb.hide()
        self.submit_log_bb.hide()
        self.back_bb.show()
        self.register_bb.hide()
        self.login_bb.hide()
        self.ll.setText('Enter the code from email.')

    def act_log(self):
        self.mail = self.email_edit.text()
        password = self.password_edit.text()
        self.email_edit.setText('')
        self.password_edit.setText('')
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        res = cur.execute("SELECT password FROM data WHERE email = ?", [self.mail]).fetchone()[0]
        con.close()
        if res == password:
            self.code = choicer()
            if self.email(self.mail):
                self.ll.setText('Email was successfully sent!\nEnter the code from email')
                self.email_edit.setText('')
                self.show_code_win()
            else:
                self.ll.setText('Incorrect address, try again')
                self.email_edit.setText('')
        else:
            self.ll.setText('Wrong email or password, try again!')

    def act_code(self):
        if self.counter > 0:
            if self.code == self.password_edit.text():
                self.ll.setText('Correct')
                self.counter = 5
            else:
                self.ll.setText(f'Incorrect.\n{self.counter} attempts left.')
                self.password_edit.setText('')
                self.counter -= 1
        else:
            self.ll.setText('0 attempts left.\nNew code sent.')
            self.password_edit.setText('')
            self.code = choicer()
            self.email(self.mail)
            self.counter = 5

    def act_reg(self):
        email = self.email_edit.text()
        password = self.password_edit.text()
        self.email_edit.setText('')
        self.password_edit.setText('')
        if email_check(email) and password_check(password):
            self.ll.setText('Successfully registered!')
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            cur.execute("INSERT INTO data(email,password) VALUES(?,?)", [email, password])
            con.commit()
            con.close()
        else:
            self.ll.setText('Incorrect email or password, try again!')

    def email(self, adress):
        gmail_user = 'sknrnx7qnbqnrcfz@gmail.com'
        gmail_password = '%&UgyQBh98MK=N2Y^+3X?@#ne%SBuvkw#nA+p9$XYpE+dB-E5CThWHp8RApa7x5s'

        sent_from = gmail_user
        to = [adress]
        subject = 'Autentification code'
        body = f'''
        Your autentification code is:
        {self.code}
        '''

        email_text = """\
                From: %s
                To: %s
                Subject: %s

                %s
                """ % (sent_from, ", ".join(to), subject, body)

        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(gmail_user, gmail_password)
            smtp_server.sendmail(sent_from, to, email_text)
            smtp_server.close()
        except Exception:
            return False
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
