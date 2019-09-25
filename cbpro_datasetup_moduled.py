import cbpro
import pandas as pd
import numpy as np
import time
from datetime import datetime, timezone

def initialize_day_data(start_time='2017-12-01', last_time='2018-12-16', granularity=75600):
    public_client = cbpro.PublicClient()

    #print("public.get_products",public_client.get_products())
    #print("public.get product trade")
    #public_client.get_product_trades(product_id='ETH-USD')
    #print("\n",public_client.get_product_trades(product_id='ETH-USD'))
    #print("\n public client_get_product_historic \n",public_client.get_product_historic_rates('ETH-USD', granularity=3600))
    #print("\n public client_get_product_24hr stats \n",public_client.get_product_24hr_stats('ETH-USD'))
    raw_data=public_client.get_product_historic_rates('ETH-USD', granularity=3600*24)

    # 3600 * 9  아홉시간  granularity를 24시간 기준으로 했을 시 오전 9시 기준으로 한다.
    # 3600 * 21 오후 21시 = 75600
    raw_dataframe = pd.DataFrame(raw_data)
    print("\n raw_dataframe.head()부분입니다 ", raw_dataframe.head() )

    # 한번에 DataFrame 의 시간부분에 9시간을 일괄적으로 뺀다.
    temp_modified_time_series= raw_dataframe.iloc[ : , 0] - 3600*9
    modified_time_series =[]
    for time in temp_modified_time_series:
        temp_timestamp=datetime.fromtimestamp( time )
        time = temp_timestamp.replace(tzinfo=timezone.utc)
        #print(time)
        modified_time_series.append(time)
    modified_price_series = raw_dataframe.iloc[ : , 1: ]

    # close 부분이 사실 price입니다.
    modified_time_dataframe=pd.DataFrame(modified_time_series)
    modified_price_dataframe=pd.DataFrame(modified_price_series)
    modified_timestamp = pd.DataFrame(temp_modified_time_series)
    # pandas concat을 통하여 앞에서 전처리한 두 DataFrame을 합쳐준다.
    modified_dataframe=pd.concat([modified_time_dataframe, modified_price_dataframe, modified_timestamp], axis=1)
    # pandas column 명을 만들고 index를 지정해 줍니다.
    # time, low, high, open, close, volume 순으로 됩니다.
    column_names = ['time', 'low', 'high', 'open', 'close', 'volume','timestamp']
    modified_dataframe.columns = column_names
    modified_dataframe.reset_index = 'time'
    print("\n modified_dataframe.의 index range index 입니다. 인덱스 문제가 생길 시 time 컬럼을 기준으로 하십시오. ")
    print("\n modified_dataframe.head() 부분으로 전처리가 모두 되어 읽을 수 있는 파일을 만듭니다,\n",modified_dataframe.head())

    # 최종 결과를 csv 파일로 저장합니다
    modified_dataframe.to_csv('get_bitcoin_data_day.csv',mode='w')

initialize_day_data(start_time='2018-01-01', last_time='2018-12-16', granularity=75600)


