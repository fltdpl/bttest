#!/usr/bin/env python3.4
import bluetooth as bt
from time import sleep
from select import select
import configparser
import random


def ConfigMap(section):
    dict1 = {}
    Config = configparser.ConfigParser()
    Config.read('config.ini')
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s!" % option)
        except:
            print("exception on %s" % option)
            dict1[option] = None
    return dict1


def connect():
    server_sock = bt.BluetoothSocket(bt.RFCOMM)
    server_sock.bind(("", bt.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    uuid = "00001101-0000-1000-8000-00805F9B34FB"

    bt.advertise_service(server_sock, "TestServer",
                         service_id=uuid,
                         service_classes=[uuid, bt.SERIAL_PORT_CLASS],
                         profiles=[bt.SERIAL_PORT_PROFILE]
                         )

    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    return server_sock, client_sock


def timer_server(q):
    sleep(15)
    q.put("sleep")


def send_data(socket):
    typ = ConfigMap("sentdata")['typ']
    path = ConfigMap("sentdata")['path']
    sdata = ConfigMap("sentdata")['sent']
    len_bytes = ConfigMap("sentdata")['bytes']
    t_wait = ConfigMap("sentdata")['delay']
    sdata_str = ""
    if typ == "random":
        hexpool = '0123456789abcdef'
        for i in range(int(len_bytes)):
            sdata = random.choice(hexpool) + random.choice(hexpool)
            sdata_str = sdata_str + chr(int(sdata, 16))
    elif typ == "data":
        if sdata:
            l = len(sdata)
            if len(sdata) >= 2:
                for i in range(int(l/2)):
                    sdata_str = sdata_str + chr(int(sdata[:2], 16))
                    sdata = sdata[2:len(sdata)]
        else:
            print("There is no data in config.ini")
            exit()

    elif typ == "path":
        if path:
            func = __import__(path)
            sdata_str = func.special_frame()
        else:
            print("There is no path in config.ini")
            exit()

    else:
        print("If you don't set data for sending in your " +
              "config.ini and, at least say 'yes' to random data!")
        exit()

    printout = ConfigMap("printout")['printsent']
    if printout == 'Hex':
        print("[sent]     "+chr_to_hex(sdata_str))
    else:
        print("[sent]     "+sdata_str)

    socket.send(sdata_str)
    sleep(float(t_wait))


def chr_to_hex(data):
    a = ""
    for x in data:
        a = a + ("0"+((hex(ord(x)))[2:]))[-2:]
    return(a)


def main():
    server_sock, client_sock = connect()
#    client_sock = 1
    while True:
        # Send Data
        send_data(client_sock)

        # Read Data
        readable, writable, exceptional = select([client_sock], [], [], 1)
        if readable:
            data = str(client_sock.recv(1024))
            data = data[2:(len(data)-1)]
            printout = ConfigMap("printout")['printresv']
            if printout == 'Hex':
                print("[Received] "+chr_to_hex(data))
            else:
                print("[Received] "+data)

    print("disconnected")
    client_sock.close()
    server_sock.close()

if __name__ == "__main__":
    main()
