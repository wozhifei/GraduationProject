from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import sys
# QtCore가 없어서 동작을 못하는건가
from PyQt5.QtCore import QCoreApplication
# from mainwindow import Ui_MainWindow

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
       
        self.islogin=None
        
        namelabel=QLabel("               아이디 입력하세요.")
        passlabel=QLabel("              비밀번호 입력하세요.")
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Log in', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.setGeometry(300,300,300,150)
        self.setWindowTitle("망고와 바나나 로그인")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(namelabel)
        layout.addWidget(self.textName)
        layout.addWidget(passlabel)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

        #아이디와 비밀번호를 전송해준다는 변수지만 그냥 한개만 쓴다.
        self.islogin =None
        self.show()

    def handleLogin(self):
        if (self.textName.text() == 'foo' and self.textPass.text() == 'bar'):
            print("Login Accepted")
            self.islogin=True
            print(" self.islogin ",self.islogin)
            #어차피 Login()에 직접 생성이면 아랫것도 필요없지않
            #self.accept()
            QCoreApplication.instance().quit

        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')
'''
class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        #super().__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

'''
if __name__ == '__main__':

    #import sys
    app = QtWidgets.QApplication(sys.argv)
    login=Login()
    sys.exit(app.exec_())
    #login =Login()인데 내가 직접 생성해서 밑에를 True로 고정시켰다.
    #잠깐만 그러면 아예 이 부분이 필요없는거 아닌가
    if login.exec_() == QtWidgets.QDialog.Accepted:
        #window = Window()
        #window.show()
        print("login.exec_() ==QtWidgets.Qdialog.Accepted")
        

