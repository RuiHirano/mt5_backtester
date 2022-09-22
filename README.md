



# Dev

- 必要なライブラリ
  - libzmq.dll(x64)
  - libsodium.dll(x64)

Testerのときはそれぞれのエージェント内のLibraryにファイルが必要かもしれない
- Tester/127.0.0.1-3000/Library/xxx

https://github.com/dingmaotu/mql-zmq から最新をもってくる

### port
127.0.0.1にする必要がある
*とかは使えない。（もしくはmt5のオプションで0.0.0.0にすればできるかも）

### Error: zmq Contextで動作が止まる。
https://github.com/zeromq/pyzmq/issues/1224

https://www.mql5.com/en/forum/339230

- どうやらContext.mqhの中のzmq_ctx_new();でブロックされている。
  - /dev/urandomを呼ぶ時にシステム内でハングしているらしい
  - windowsならできる？

- RemoteのWindows環境だとエラーなくできた
  - Windowsじゃないとシステムコールでハングされる？

### MT5フォルダの場所
'/Applications/MetaTrader 5.app/Contents/MacOS/MetaTrader 5' '/config:/System/Volumes/Data/Users/ruihirano/Library/Application Support/MetaTrader 5/Bottles/metatrader5/drive_c/Program Files/MetaTrader 5/Config/config.ini'

'/System/Volumes/Data/Users/ruihirano/Library/Application Support/MetaTrader 5/Bottles/metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Experts/MT5BacktesterEA.mq5'

### unbindされずport が残っている場合
次回のbindでエラーが発生する
```
netstat -aon | find "5556"
taskkill /pid <kill したい PID>
```

python workspace\mt5_backtester\examples\basic.py

一度killしてから行えばstream、apiも動く
