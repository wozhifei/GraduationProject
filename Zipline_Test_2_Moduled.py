# 이전은 웹데이터를 기반이고 지금은 로컬 데이터인 get_bitcoin_data_day.csv 파일에서 읽는다.

'''
    중요 !
    Dataframe에서 한 줄만 추출하려고 할 때 data[[ ' 이름']] 괄호를 두 개 줘야 데이터 프레임으로 된다.
    컬럼 이름이 사라질 수 있다.
'''

import pandas_datareader.data as web
import datetime
import time
from datetime import  timedelta
import matplotlib.pyplot as plt
from zipline.api import order_target, record, symbol
from zipline.algorithm import TradingAlgorithm
import numpy as np
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
import cbpro_datasetup_moduled as gdax
import pandas as pd

def algo_trade():
    # 아래는 가상거래 알고리즘을 동작시킬 시 true_divide Error를 무시한다는 내용이다.
    np.seterr(divide='ignore', invalid='ignore')

    # get_bitcoin_data_day.csv. 파일을 읽는다. 파일은 오늘을 기준으로 1년치가 보여진다.
    bithistory = pd.read_csv("./get_bitcoin_data_day.csv", parse_dates=True, index_col='time')
    bithistory = bithistory.sort_index(ascending=True)
    #print("bitcoin day History \n\n",bithistory,"\n\n")
    #print("bitcoin day History Index \n\n",bithistory.index.tolist(),"\n\n")
    print("Zipline_Test_2_Mouduled.py의 bithistory.head()\n",bithistory)
    # bithistory에서 close 컬럼을 추출하기 위해 [[ ]] 두 개로 해줘야 한다.
    bitclose=bithistory[['close']]

    
    
    #print("bitcoin day Close Price \n\n",bitclose,"\n\n")

    #타임존을 변경하려면 9시였는데 이걸 0시로 일단 바꿔주자.
    # 시간이 달라서 찾을 수가 없다는데?
    #print("bitcoin day Close TimeChanged@ \n\n",bitclose,"\n\n")


    #datetime
    #temp_datetime=datetime.fromtimestamp(bitclose.index.tolist()[0])
    #print(str(bitclose.index.tolist()[0]))
    #print(str( bitclose.index.tolist()[0] )[0])
    
    # 이미 cbpro_datasetup_moduled에서 만들었다.
    # 인덱스 수정은 cbpro_datasetup_moduled를 참조할것

    
    # 인덱스 수정
    TimeIndex=[]
    for temptime in bithistory.index.tolist():
        temptime_str = str(temptime)[0:110]
        temptime_datetime = datetime.datetime.strptime(temptime_str,"%Y-%m-%d %H:%M:%S")
        #utc_datetime = temptime_datetime.replace(tzinfo=datetime.timezone.utc)
        TimeIndex.append(temptime_datetime)

    #TimeIndex.append( 맨 마지막   내일거까지 해야된다고?
        
    print("\n\n Zipline_Test_2_Moduled.py 의 TimeIndex의 값 \n\n",TimeIndex)


    # Zipline을 적용하기 위해서는 무조건 UTC 시계로 타임존을 변경해야한다.
    #bitclose =bitclose.tz_localize("UTC")
    #print("Close Price  Time Zone Modified \n\n", bitclose ,"\n\n")
    #print(bitclose.index.tolist()[0])
    #print(bitclose.index.tolist()[1])
    #print(type(bitclose.index.tolist()[0]))

    #만들어진 TimeIndex와 value값을 이용해서 다시 만들자
    #아래는 작동 안된다.
    #????? TimeIndex = time.mktime(TimeIndex.timetuple()).tz_localize('UTC')

    new_data_dict={"close": bitclose.loc[:,'close'].values }
    new_data = pd.DataFrame(new_data_dict, index=TimeIndex)
    print(new_data)
    
    #
    new_data=new_data.tz_localize("UTC")
    print("UTC로 변경된 new_data\n",new_data)
    
    #이후 algo.run에서 사용할 start 날짜와 end 날짜를 저장한다.
    start = new_data.index[0]
    end = new_data.index[-1]
    print("start 의 값 : : ",start)
    print("start 의 타입 : ", type(start))
    print("end 의 값 : : ",end)
    print("end 의 타입 : ", type(end))
    
        # 실제 이동선 평균 알고리즘을 위한 테스트
    def initialize(context):
        context.i = 0
        #context.sym = symbol('BTC')
        #Basic 튜토리얼을 보고 수정 https://www.zipline.io/beginner-tutorial.html
        #데이터 프레임 중 어느 컬럼을 보고 값을 결정할 것인가.
        context.asset = symbol('close')
        # 시뮬레이션 초기의 값에 화폐를 보유하고 있는 지 설정
        context.hold = False
        

    def handle_data(context, data):
        context.i += 1
        if context.i < 20:
            return
        
        buy = False
        sell= False

        ma5 = data.history(context.asset, 'close', 5, '1d').mean()
        ma20 = data.history(context.asset, 'close', 20, '1d').mean()


        '''
        수정 이전의 이동평균선 전략
        if ma5 > ma20:
            order_target(context.asset, 1)
        else:
            order_target(context.asset, -1)
        '''
        #수정 이후의 이동평균선 전략
        # 구현한 전략과의 차이는 매수/매도가 일정 "구간" 동안 이뤄지는 것이
        # 아니라 골든크로스/데드크로스 시점에서만 발생한다는 것입니다.
        if ma5 > ma20 and context.hold==False:
            order_target(context.asset, 10)
            context.hold = True
        elif ma5 < ma20 and context.hold == True:
            order_target(context.asset, -10)
            context.hold = False

       
        record(BTC=data.current(context.asset, "close"), ma5=ma5, ma20=ma20)
     
            
    # initialize와 handle_data가 사용되기 전에 위에 정의해 둬야한다.    
    algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data, start=start , end=end)
    result = algo.run(new_data)

    print(result)
    #result[['ma5','ma20']].plot()
    #result[['portfolio_value']].plot()

    fig=plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)

    ax1.plot(result[['ma5']], label='5 days')
    ax1.plot(result[['ma20']], label='20 days')
    ax1.set_ylabel("BitCoin Price")
    ax1.legend(loc='upper right')

    ax2.plot(result[['portfolio_value']],label='Money', color='g')
    ax2.set_ylabel("Profit")
    ax2.legend(loc='upper right')
    plt.title('이동평균선 수정 Bitcoin 10 단위')

    plt.show()


algo_trade()
