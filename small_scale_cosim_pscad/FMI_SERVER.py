from __future__ import print_function
import sys, os
import logging

# import stuff related to PSCAD Automation controller
#sys.path.append(r"C:\Program Files (x86)\PSCAD\Automation\Lib\mhrc")
#import win32
#import automation.controller
#from win32com.client.gencache import EnsureDispatch as Dispatch
#import xml.etree.ElementTree as ET
#import win32com.client
#import shutil

import time
import struct
from threading import Thread

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor


class fmu():
    inputs = {}
    outputs = {}
    cur_time = 0.0
    master_time = 0.0
    
    
class FMI_Server(Protocol):
    #def __init__(self):
        #super(Protocol, self).__init__()
    

    def dataReceived(self, data):
        # "GET" Request from pscad_recv
        if data[0] in ["G", ord("G")]:
            num = int(data[3])
            # Python3 hack to handle byte-data
            if num > 48: num = int(chr(num))

            # Wait some time before responding, so master can do its tasks
            while fmu.cur_time >= fmu.master_time:
                time.sleep(0.0001)
            resp = struct.pack("d"*num,*fmu.inputs[fmu.cur_time])
            self.transport.write(resp)


        # "SET" request from pscad_send
        if data[0] in ["S", ord("S"),"R", ord("R")]:           
            # Convert binary data to array of floats
            data_dict = struct.unpack("d"*(len(data)//8), data[4:])

            # First value is time
            tmp = round(float(data_dict[0]),2)
            
            if len(data_dict) > 1:
                # Set outputs for time step
                fmu.outputs[tmp] = data_dict[1:]

                # Dirty hack: sometimes send/receive happen in wrong order so use 
                # value from previous time step.This will be overwritten in elsewhere
                fmu.inputs[tmp] = fmu.inputs[fmu.cur_time]
                fmu.cur_time = tmp


        # Close TCP socket
        self.transport.loseConnection()


    def instantiate(self):
        f = Factory()
        f.protocol = FMI_Server
        reactor.listenTCP(8001, f)

        
    def initialize(self, initial_inputs):
        fmu.cur_time = 0.0
        fmu.inputs[fmu.cur_time] = initial_inputs
        print("Initial input values for PSCAD: ", fmu.inputs[0.0])
        print("You can now start the simulation in PSCAD")

        # Start TCP server in background
        Thread(target=reactor.run, args=(False,)).start()
    
        '''while True:
            try:
                t = fmu.cur_time
                #print("outputs: ",t, fmu.outputs[t])
                fmu.inputs[t] = [t, -1*t]
                #print("inputs: ", t, fmu.inputs[t])
                time.sleep(0.001)

            except KeyError: pass
            #reactor.callFromThread(twistedServer.sendResponse, response)'''



    ''''def connectionMade(self):
        print("connection made")

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols-1
        print("connection lost", reason)'''

'''inputs = {}
outputs = {}
current_time = 0.0'''

def main():

    fmu_s = FMI_Server()
    fmu_s.instantiate()
    fmu_s.initialize()

if __name__ == '__main__':
    main()
