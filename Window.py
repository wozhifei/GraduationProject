import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
import graphsetupui
import logindialogue


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 프로그램 종료 버튼
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        #exitAction.triggered.connect(qApp.quit)
        #exitAction.triggered.connect(qApp.exit)
        exitAction.triggered.connect(QCoreApplication.instance().quit)

        # Log in 버튼
        loginAction = QAction('Log In', self)
        loginAction.setShortcut('Ctrl+L')
        loginAction.setStatusTip('로그인합니다')
        loginAction.triggered.connect(self.loginaction)

        # Log out 홈페이지 접속 버튼
        logoutAction = QAction('Log Out', self)
        logoutAction.setShortcut('Ctrl+O')
        logoutAction.setStatusTip('로그아웃 접속합니다')
        loginAction.triggered.connect(self.logoutaction)

        #Korbit 홈페이지 접속 버튼
        korbitAction = QAction('Korbit', self)
        korbitAction.setShortcut('Ctrl+K')
        korbitAction.setStatusTip('Korbit 홈페이지 접속합니다')
        #loginAction.triggered.connect()

        #Coinbase 홈페이지 접속  버튼
        coinbaseAction = QAction('Coinbase', self)
        coinbaseAction.setShortcut('Ctrl+C')
        coinbaseAction.setStatusTip('Log Out')
        #logoutAction.triggered.connect()

        #종목 선택
        # 화폐 종류 BTC로 설정
        targetBTCAction = QAction('비트 코인', self)
        targetBTCAction.setShortcut('Alt+C')
        targetBTCAction.setStatusTip('비트 코인으로 종목 변경 ')

        # 화폐 종류 XRP로 변경
        targetXRPAction = QAction('리플', self)
        targetXRPAction.setShortcut('Alt+R')
        targetXRPAction.setStatusTip('리플로 종목 변경')

        # 선형, 막대형 그래프 설정
        # 선형 그래프 설정
        linegraphAction = QAction('선형 그래프', self)
        linegraphAction.setShortcut('Alt+L')
        linegraphAction.setStatusTip('Line Graph')

        # 막대형 그래프
        bargraphAction = QAction('막대 그래프', self)
        bargraphAction.setShortcut('Alt+B')
        bargraphAction.setStatusTip('Bar Graph')
        
        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&일반')
        fileMenu.addAction(loginAction)
        fileMenu.addAction(logoutAction)
        fileMenu.addAction(exitAction)

        targetMenu = menubar.addMenu('&종목 선택')
        targetMenu.addAction(targetBTCAction)
        targetMenu.addAction(targetXRPAction)
        
        graphMenu= menubar.addMenu('&그래프')
        graphMenu.addAction(linegraphAction)
        graphMenu.addAction(bargraphAction)

        infoMenu=menubar.addMenu('&정보')
        infoMenu.addAction(korbitAction)
        infoMenu.addAction(coinbaseAction)
        
        self.setWindowTitle('가상 화폐 자동 거래 프로그램')
        self.setGeometry(100, 100, 1230, 670)

        #내부 배치를 위해 gridLayout을 추가한다.
        grid=QGridLayout()
        self.setLayout(grid)

        #그리드 레이아웃 속에 우리가 만든 Widget을 넣는다.
        graphui=graphsetupui.MyWindow(parent=self)
        grid.addWidget(graphui,0,0)
        self.show()

    # 메뉴 부분의 Action 정의
    def loginaction(self):
        #works fine
        '''print("login Action is triggered")
        inputid, ok=QInputDialog.getText(self, '제목 다이얼로그', "Enter Your ID")

        if ok:
            print("QInputDialog도 문제네?   ", str(inputid) )'''
        # 로그인을 해서 성공했는 지 반환 받는 부분
        loginTest=logindialogue.Login(parent=self)
        loginTest.exec_()

        #islogin=loginTest.islogin
        #if( islogin==True):
            #sys.exit(loginTest.exec_())
        print(islogin)
        
        
    def logoutaction(self):
        print("logout Action is triggered")
        if islogin==True:
            islogin=False
            print("로그아웃 완료")
            
        elif islogin != True or islogin==None:
            print("이미 로그아웃 상태입니다")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())






