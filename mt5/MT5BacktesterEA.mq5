//+------------------------------------------------------------------+
//|                                              MT5BacktesterEA.mq5 |
//|                                  Copyright 2022, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2022, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"

#include <Zmq/Zmq.mqh>
// allow webrequest http://127.0.0.1:5556, http://127.0.0.1:5557
input string APIServer = "tcp://localhost:5557";  // api server ip
input string StreamServer = "tcp://localhost:5556";  // stream server ip

string api_server        = "";
string stream_server        = "";

//--- Globales ZMQ
string appname = "MT5BacktesterEA";
Context context(appname);
Socket  stream_socket(context, ZMQ_REQ);
Socket  api_socket(context, ZMQ_REP);

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   Print("OnInit2: ");
   if (DetectEnvironment() == false)
    {
    Alert("Error: The property is fail, please check and try again.");
    return(INIT_FAILED);
    }
   StartZmq();
//---
    string response = "";
    string request = StreamDataToJsonString("ON_INIT", "{}");
    bool result = ZmqRequest(&stream_socket, request, response);
    if(result){
        Print("Response: ", response);
    }else{
        Print("Error: ", GetLastError());
    }
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
    string response = "";
    string request = StreamDataToJsonString("ON_DEINIT", "{}");
    bool result = ZmqRequest(&stream_socket, request, response);
    if(result){
        Print("Response: ", response);
    }else{
        Print("Error: ", GetLastError());
    }
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
    if(IsNewBar(Symbol(), PERIOD_M5)){     
      MqlTick tick;
      bool ok = GetCurrentTick(tick);
      if (ok)
      {
        Print("Tick: ", tick.ask);
        string response = "";
        string tick_json = TickToJsonString(tick);
        string request = StreamDataToJsonString("ON_TICK", StringFormat(
          "{ \"tick\": %s}", tick_json));
        bool result = ZmqRequest(&stream_socket, request, response);
        if(result){
            Print("Response: ", response);
        }else{
            Print("Error: ", GetLastError());
        }
      }
    }
  }
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//| Detect the script parameters                                     |
//+------------------------------------------------------------------+
bool DetectEnvironment()
  {
    if (APIServer == "" || StreamServer == "") 
      return false;
    
    api_server        = APIServer;
    stream_server        = StreamServer;
    return true;
  }


//+------------------------------------------------------------------+
//| Start the zmq server                                             |
//+------------------------------------------------------------------+
void StartZmq()
  {  
    if (api_server == "" || stream_server == "")
      return;
      
    Print("Connecting to api server…");
    stream_socket.connect(stream_server);

    /*Print("Build api server…");
    int result = api_socket.bind(stream_server);
    if (result != 1)
      {
        Alert("Error: Unable to bind server, please check your port.");
        return;
      }*/
  }


//+------------------------------------------------------------------+
//| Push the message for all of the subscriber                       |
//+------------------------------------------------------------------+
bool ZmqRequest(Socket *socket, const string req_message, string res_message)
  {
    ZmqMsg request(req_message);
    PrintFormat("Sending %d...",req_message);
    socket.send(request);

    // Get the reply.
    ZmqMsg reply;
    socket.recv(reply);
    res_message=reply.getData();
    PrintFormat("Received %d",res_message);
    return true;
  }

//+------------------------------------------------------------------+
//| Get Current Tick                                                 |
//+------------------------------------------------------------------+
bool GetCurrentTick(MqlTick &tick)
  {
    MqlTick ticks[];
    if (CopyTicks(Symbol(), ticks, COPY_TICKS_ALL, 0, 1) == 1)
      tick = ticks[0];
      return true;
    return false;
  }

//+------------------------------------------------------------------+
//| Convert Tick to Json                                               |
//+------------------------------------------------------------------+
string TickToJsonString(MqlTick &tick)
  {
    return StringFormat(
          "{ \"time\": \"%s\",\"bid\": %f,\"ask\": %f,\"last\": %f,\"volume\": %d,\"time_msc\": %d,\"flags\": %d,\"volume_real\": %f}",
          TimeToString(tick.time, TIME_DATE|TIME_SECONDS),
          tick.bid,
          tick.ask,
          tick.last,
          tick.volume,
          tick.time_msc,
          tick.flags,
          tick.volume_real
        );
  }

//+------------------------------------------------------------------+
//| Convert StreamData to Json                                               |
//+------------------------------------------------------------------+
string StreamDataToJsonString(string event, string data)
  {
    return StringFormat(
          "{ \"event\": \"%s\",\"data\": %s}",
          event,
          data
        );
  }


bool IsNewBar(string symbol, ENUM_TIMEFRAMES tf)
{
   static datetime time = 0;
   if(iTime(symbol, tf, 0) != time)
   {
      time = iTime(symbol, tf, 0);
      return true;
   }
   return false;
}
