import struct
import logger
#import flask_qr
# import flask_api
import time
from queue import Queue 
from threading import Thread 
from speech2text import Speech2Text
from sockets import UDPSocketServer
from translator import Translator


class Client:
    def __init__(self, ip):
        self.IP = ip
        self.QUEUE = Queue() 
        self.resp_event = False
        self.response = ""
        
    def add_response(self, resp):
        self.response = resp
        self.resp_event = True




class Server:

    def __init__(self, app_logger):
        self.received_data = []
        self.MAX_SIZE_OF_REC = 10000
        self.clients = []
        # self.number_of_users = 0
        #self.queues = []
        #self.resonses = []
        self.app_logger = app_logger
    

    def run(self):
        self.soc_serv = UDPSocketServer(self.app_logger)
        self.transl = Translator(self.app_logger)
        self.app_logger.info("server started")
        while True:
            message, address = self.soc_serv.recv()
            for client in self.clients:
                if address[0] == client.IP:
                    client_queue = client.QUEUE
                    client_queue.put(message)
            # if address[0] in self.clients.IP:
            #     user_queue = self.queues[self.users.index(address[0])]
            #     user_queue.put(message)
            # else:
            #     self.app_logger.info("unknown user")
            #     self.app_logger.info(address[0])
            #     self.app_logger.info(self.users)
                # self.handle_new_user(message, address) 

    def add_client(self, ip):
        self.app_logger.info("adding new client")
        new_client = Client(ip)
        self.clients.append(new_client)
        # self.app_logger.info("creating new queue for this user")
        # new_queue = Queue() 
        # self.queues.append(new_queue)
        # self.number_of_users +=1
        new_thread = Thread(target = self.user_thread, name="user", args =(new_client, ), daemon=True)
        self.app_logger.info("starting new client thread...")
        new_thread.start()
               


    # def handle_new_user(self, message, address):
    #     self.app_logger.info("new user handeling beggins")
    #     token = flask_qr.get_token()
    #     try:
    #         str_mes = message.decode('UTF-8')
    #     except:
    #         self.app_logger.info("received wrong data (TOKEN)")
    #     else:
    #         if str_mes == token:
    #             self.app_logger.info("received right token")
    #             self.users.append(address)
    #             self.app_logger.info("creating new queue for this user")
    #             new_queue = Queue() 
    #             self.queues.append(new_queue)
    #             self.number_of_users +=1
    #             new_thread = Thread(target = self.user_thread, name="user"+str(self.number_of_users), args =(new_queue, address, ), daemon=True)
    #             self.app_logger.info("starting new user thread...")
    #             new_thread.start()
    #             time.sleep(0.1)
    #             bytesToSend = "START".encode('UTF-8')
    #             self.soc_serv.send(bytesToSend, address)
    #             self.app_logger.info("Data \""+bytesToSend.decode('UTF-8')+"\" was send to "+str(address)+"len: "+str(len(bytesToSend)))
    #         else:
    #             self.app_logger.info("received wrong token")


    def user_thread(self, client):
        # self.app_logger.info("user thread started sucesfully")
        # self.app_logger.info("waiting for START message")
        # message = queue.get()
        # try:
        #     str_mes = message.decode('UTF-8')
        # except:
        #     self.app_logger.info("received wrong data (START)")
        #     queue.task_done()
        # else:
        #     if str_mes == "START":
        #         queue.task_done() 
        #         self.app_logger.info("received data START")
        self.app_logger.info("start receiving data...")
        self.app_logger.info("starting speech2text...")
        self.s2t = Speech2Text(self.app_logger)
        self.s2t.start()
        for i in range(self.MAX_SIZE_OF_REC):
            message = client.QUEUE.get() 
            try:
                str_mes = message.decode('UTF-8')
            except:
                self.s2t.process(message)
                client.QUEUE.task_done()
            else:
                if str_mes == "STOP":
                    self.app_logger.info("received data STOP")
                    self.app_logger.info("stop receiving data")
                    client.QUEUE.task_done() 
                    break
                    
        self.app_logger.info("stoped speech2text")
        self.s2t.stop()
        outcome_string = self.s2t.get_outcome()
        self.app_logger.info("best hypothesis: \""+outcome_string+"\"")
        translated_output_pol = self.transl.translate(outcome_string, "pol")
        self.app_logger.info("translated to : \""+translated_output_pol+"\"")
        string_to_send = outcome_string + "\n" + translated_output_pol

        client.add_response(string_to_send)
        self.app_logger.info("added response : \""+string_to_send+"\"")
        
        # bytesToSend = string_to_send.encode('UTF-8')
        # self.soc_serv.send(bytesToSend, address)
        # self.app_logger.info("Data \""+bytesToSend.decode('UTF-8')+"\" was send to "+str(address))

        # self.app_logger.info("Deleting this client from list")
        # self.clients.remove(client)
        # self.users.remove(address)
        # self.app_logger.info("Deleting this user's queue from list")
        # self.queues.remove(queue)
        # self.app_logger.info("Ending this user handling")

    def get_response(self, ip):
        self.app_logger.info("Start get_response() function for "+ip)
        for client in self.clients:
            if client.IP == ip:
                while True:
                    if client.resp_event == True:
                        response = client.response
                        self.app_logger.info("Deleting this client from list")
                        self.clients.remove(client)
                        return response
                    time.sleep(0.1)

        


