import zmq

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5556")

    print("Server startup.")

    while True:
        message = socket.recv_string()
        print("Received message = %s" % message)
        socket.send_string("Reply: %s" % message)

    socket.close()
    context.destroy()
    
if __name__ == "__main__":
    start_server()
