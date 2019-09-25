'''
UI Layout 초안

디자인 초안에서 6시간 간격이 아닌 1일치를 해보자

'''
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
#왠지 모르게 밑에는 더 이상 동작하지 않아 새로운 라이브러리를 사용
#import gdax_filefetch_day as gdax
import cbpro_datasetup_moduled as gdax
import Zipline_Test_2 as zt
import Zipline_Test_2_Moduled as zt2

#현재 시간을 초기화 해줍니다. 만약 일정 기간으로 한정하고 싶다면 start_time 부분에서 now.day를 -날짜를 해줄것
now=datetime.now()
print("\n now : ",now)
last_time = '%s-%s-%s' % (now.year, now.month, now.day)
if( now.day >7):
    start_time= '%s-%s-%s' % (now.year, now.month, now.day - 7)
elif (now.day<=7):
    start_time= '%s-%s-%s' % (now.year, now.month, now.day-now.day+1)
    
print(start_time)
print(last_time)

class MyWindow(QWidget):
    #단위 테스트를 하려면 parent가 당연히 없어야겠다
    def __init__(self, parent):
    #def __init__(self):
        super().__init__()
        self.setParent(parent)
        self.setupUI()
        # 과거 데이터를 초기화합니다. start_time='2018-11-09', last_time='2018-11-12',granularity=3600이 기본입니다. 1시간봉가져옵니다.
        print("Initialize에 들어가는 start_time  = ",start_time,"\nInitialize에 들어가는 last_time = ",last_time,"\n")
        start_time
        gdax.initialize_day_data(start_time=start_time, last_time=last_time)
        
    def setupUI(self):
        #self.statusBar()
         #메뉴바 생성
        #menubar=self.menuBar()
        #fileMenu = menubar.addMenu('&일반')
        #fileMenu.addAction()
        #loginMenu = QMenu('Log In',self)
        #logoutMenu=QMenu('Log out',self)
        #loginMenu.addAction()
        #logoutMenu.addAction()

        # 부모의 윈도우에 들어가는 것이므로 아래는 주석처리한다. 단독으로 쓰일 때는 필요하겠지만        
        self.setGeometry(20, 50, 1200, 600)
        #self.setWindowTitle("망고와 바나나")
        #self.setWindowIcon(QIcon('icon.png'))
       
        self.lineEdit = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit3 = QLineEdit()
                
        self.pushButton = QPushButton("차트그리기")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.pushButton2 = QPushButton("자동 거래 시작")
        self.pushButton2.clicked.connect(self.pushButtonClicked2)
        self.pushButton3 = QPushButton("자동 거래 종료")
        self.pushButton3.clicked.connect(self.pushButtonClicked3)
        self.pushButton4 = QPushButton("수동 구매")
        self.pushButton4.clicked.connect(self.pushButtonClicked4)
        self.pushButton5 = QPushButton("수동 판매")
        self.pushButton5.clicked.connect(self.pushButtonClicked5)


        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.canvas)

        # Right Layout
        rightLayout = QVBoxLayout()
        
        rightLayout.addWidget(self.pushButton)
        #자동 거래 시작 부분
        rightLayout.addWidget(self.pushButton2)

        #자동 거래 종료 부분
        rightLayout.addWidget(self.pushButton3)

        #수동 거래를 위한 수량 추가 부분
        #기본적으로 Bitcoin을 대상으로 하기 때문에 아래의 부분은 삭제했습니다.
        textLabel1=QLabel("\n        수동 구매 수량")
        rightLayout.addWidget(textLabel1)
        #수동 구매를 위한 수량 받는 self.lineEdit 창
        rightLayout.addWidget(self.lineEdit)
        #수동 구매를 위한 시작 버튼
        rightLayout.addWidget(self.pushButton4)
        textLabel1=QLabel("\n        수동 판매 수량")
        rightLayout.addWidget(textLabel1)
        #수동 판매를 위한 수량 받는 self.lineEdit 창
        rightLayout.addWidget(self.lineEdit2)
        #수동 판매를 위한 시작 버튼
        rightLayout.addWidget(self.pushButton5)
        
        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)
        
        self.setLayout(layout)
        df= pd.read_csv('./get_bitcoin_data_day.csv', parse_dates=True, index_col='time')
        print("graphsetupui의 pd.read_csv 입니다. ",df.head())
        

        #부모 Window 속에서 show를 하기 위해 여기서 show를 대신한다.
        self.show()
        
    def pushButtonClicked(self):
        #먼저 이전에 있었던 Graph들을 초기화 한다.
        #아마도 제대로 clear가 되는 듯 싶다.
        self.fig.clf()

        #얻고 싶은 시작 데이터 날짜와 종료 위치를 구한다. end는 기본적으로 최신 None값
        # 내림차순으로 정렬되어 있기 때문에 start end가 다르다
        start= -12
        end= None
        
        # time, low , high, open, close, volume 순으로 된다. index_col=0으로 지정했기 때문에 앞으로는 0은 price부터 시작한다.
        #  parse_dates=True 속성을 지워본다.
        #dateparse = lambda dates: [pd.datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in dates]
        df= pd.read_csv('./get_bitcoin_data_day.csv',index_col='time')
        df=df.sort_index(ascending=True)
        #df.index = df.iloc[:]
        print("graphsetupui.py df.index는 아래와 같습니다")
        print(df.index)
        print("\n graphsetupui.py df는 아래와 같습니다 ")
        print(df.head())

        
        print("==================이미 만들어진 시간을 더 보기 좋게 월 일 시간으로 바꿉니다. ===============")
        x_axis_date_hour=[]
        temp=""
        for i in df.index :
            temp=i[5:10]+" "+i[11:13]+''
            x_axis_date_hour.append(temp)
            temp=""
        print(x_axis_date_hour)
        
        #아 평균값을 구할 필요 없다.
        #df['1 Hour Price'] = df.iloc[ : , 4].rolling(window=20).mean()
        #df['1 Hour Volume'] = df.iloc[ : , 5].rolling(window=20).mean()
       
        
        #원하는 종목의 가격을 나내는 그래프
        price_graph = self.fig.add_subplot(211)
        #이전에는 아래와 같은 형태를 x축으로 사용
        #price_graph.plot(df.index[start : end], df.iloc[start : end, 3], label='1 Hour Price')
        price_graph.plot(x_axis_date_hour[start : end], df.iloc[start : end, 3], label='1 Day Price / USD',color='r')
        price_graph.legend(loc='upper right')
        price_graph.set_ylabel(" 가격 ")
        price_graph.set_xlabel(" 날짜 ")
        price_graph.grid()
        #거래량을 나타내는 그래프
        volume_graph = self.fig.add_subplot(212)
        #이전에는 아래와 같은 형태를 x축으로 사용
        #volume_graph.plot(df.index[start : end], df.iloc[ start : end, 4], label='1 Hour Volume')
        volume_graph.plot(x_axis_date_hour[start : end], df.iloc[ start : end, 4], label='1 Day Volume', color='b')
        volume_graph.legend(loc='upper right')
        volume_graph.set_xlabel(" 날짜 ")
        volume_graph.set_ylabel(" 거래량 ")
        volume_graph.grid()
        self.canvas.draw()
        
    #자동거래 시작 버튼
    def pushButtonClicked2(self):
        self.fig.clf()
        algoresult=zt2.algo_trade()
        print(algoresult)
    #자동 거래 종료 버튼
    def pushButtonClicked3(self):
        #정상적인 종료는 아닌 듯 하다. 제대로 만들
        #강제적으로 프로그램을 종료하지 않고 플래그를 써서 종료를 시키자.
        # 나중에 sys.exit(ret)는 수정할 것.
        sys.exit(ret)

    #수동 구매를 진행하기 위한 함수로 수동 구매가 아래에 들어간다.
    def pushButtonClicked4(self):
        sys.exit(ret)
        
    #수동 판매를 진행하기 위한 함수.
    def pushButtonClicked5(self):
        sys.exit(ret)


        
'''
# 단위 테스트를 하기 위해서는 여기를 주석 처리 해제하고 F5를 눌르세
#삽입을 하기 위해 커스텀 위젯을 만들어야 하므로 여기는 아니다.
#더 큰 Window 내부에서 콜을한다.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window=MyWindow()
    window.show()
    ret=app.exec_()
'''
#def graphui(parent):
    # MainWindow에서 전달 받은 QApplication을 받는다.
    #app2 = QApplication(sys.argv)
    #window=MyWindow(parent)
    #또한 여기서 window.show를 하지 않고 setup에서 show를 한다.
    #window.show()
    #ret=app.exec_()
    #ret = app2.exec_()
#테스트
