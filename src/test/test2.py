from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
 
# MetaTrader 5に接続する
if not mt5.initialize():
   print("initialize() failed")
   mt5.shutdown()
 
# 接続状態とパラメータをリクエストする
print(mt5.terminal_info())
# MetaTrader 5バージョンについてのデータを取得する
print(mt5.version())
 
# EURAUDから1,000ティックをリクエストする
euraud_ticks = mt5.copy_ticks_from("EURAUD", datetime(2020,1,28,13), 1000, mt5.COPY_TICKS_ALL)
# AUDUSDから2019.04.01 13:00 - 2019.04.02 13:00のティックをリクエストする
audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2020,1,27,13), datetime(2020,1,28,13), mt5.COPY_TICKS_ALL)
 
# 数々の方法で異なる銘柄からバーを取得する
eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(2020,1,28,13), 1000)
eurgbp_rates = mt5.copy_rates_from_pos("EURGBP", mt5.TIMEFRAME_M1, 0, 1000)
eurcad_rates = mt5.copy_rates_range("EURCAD", mt5.TIMEFRAME_M1, datetime(2020,1,27,13), datetime(2020,1,28,13))
 
# MetaTrader 5への接続をシャットダウンする
mt5.shutdown()
 
#データ
print('euraud_ticks(', len(euraud_ticks), ')')
for val in euraud_ticks[:10]: print(val)
 
print('audusd_ticks(', len(audusd_ticks), ')')
for val in audusd_ticks[:10]: print(val)
 
print('eurusd_rates(', len(eurusd_rates), ')')
for val in eurusd_rates[:10]: print(val)
 
print('eurgbp_rates(', len(eurgbp_rates), ')')
for val in eurgbp_rates[:10]: print(val)
 
print('eurcad_rates(', len(eurcad_rates), ')')
for val in eurcad_rates[:10]: print(val)
 
#PLOT
# 取得したデータからDataFrameを作成する
ticks_frame = pd.DataFrame(euraud_ticks)
# 秒での時間をdatetime形式に変換する
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
# チャートにティックを表示する
plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')
 
# 凡例を表示する
plt.legend(loc='upper left')
 
# ヘッダを追加する
plt.title('EURAUD ticks')
 
# チャートを表示する
plt.show()
