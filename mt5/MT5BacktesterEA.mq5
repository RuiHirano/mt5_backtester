//+------------------------------------------------------------------+
//|                                       JiowclSubscriberClient.mq5 |
//|                                Copyright 2017-2021, Ji-Feng Tsai |
//|                                        https://github.com/jiowcl |
//+------------------------------------------------------------------+
#property copyright   "Copyright 2021, Ji-Feng Tsai"
#property link        "https://github.com/jiowcl/MQL-CopyTrade"
#property version     "1.12"
#property description "MT5 Copy Trade Subscriber Application. Subscribe order status from source signal trader."
#property strict

#include <Zmq/Zmq.mqh>
input string Server = "tcp://localhost:5556";  // Subscribe server ip
input uint   ServerDelayMilliseconds = 300;                     // Subscribe from server delay milliseconds (Default is 300)
input bool   ServerReal              = false;                   // Under real server (Default is false)

//--- Globales Application
const string app_name    = "Jiowcl Expert Advisor";

//--- Globales ZMQ
Context context;
Socket  socket(context, ZMQ_REQ);

string zmq_server        = "";
uint   zmq_subdelay      = 0;
bool   zmq_runningstatus = false;

int OnInit()
  {
//---
   Print("OnInit: ");
   if (DetectEnvironment() == false)
    {
    Alert("Error: The property is fail, please check and try again.");
    return(INIT_FAILED);
    }
   StartZmqClient();
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
    //StopZmqClient();
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   Print("OnTick");
   
  }

//+------------------------------------------------------------------+
//| Detect the script parameters                                     |
//+------------------------------------------------------------------+
bool DetectEnvironment()
  {
    if (Server == "") 
      return false;
    
    zmq_server        = Server;
    zmq_subdelay      = (ServerDelayMilliseconds > 0) ? ServerDelayMilliseconds : 10;
    zmq_runningstatus = false;
    return true;
  }
//+------------------------------------------------------------------+
//| Start the zmq client                                             |
//+------------------------------------------------------------------+
void StartZmqClient()
  {
    if (zmq_server == "") 
      return;
    
    int result = socket.connect(zmq_server);
    
    if (result != 1)
      {
        Alert("Error: Unable to connect to the server, please check your server settings.");
        return;
      }
    
    for(int request_nbr=0; request_nbr!=10 && !IsStopped(); request_nbr++)
     {
      ZmqMsg request("Hello");
      PrintFormat("Sending Hello %d...",request_nbr);
      socket.send(request);

      // Get the reply.
      ZmqMsg reply;
      socket.recv(reply);
      PrintFormat("Received World %d",request_nbr);
     }
  }

