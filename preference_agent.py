from data_communication import ReadWriteUserData
from enum import Enum
import multiprocessing


class MessageEnum:
    # __order__ = 'END READ WRITE'
    END = 'end'
    READ = 'read'
    WRITE = 'write'


class PreferenceAgent:

    def __init__(self, connection):
       self.read_write_data = ReadWriteUserData('./users_profile')
       self.profiles = self.read_write_data.read_file()
       self.connection = connection


    def read_msg(self):
        while 1:
            msg  = self.connection.recv()
            if msg == MessageEnum.END:
                break
            print(self.profiles)

    def send_msg(self):
        self.connection.send('Text')
        self.connection.send(MessageEnum.END)

def send_msgs(conn, msgs):
    for msg in msgs:
        conn.send(msg)
    conn.close()

def recv_msg(conn):
    print('ehee')
    while 1:
        msg = conn.recv()
        if msg == MessageEnum.END:
            break
        print(msg)

parent_conn, child_conn = multiprocessing.Pipe()

msgs = [MessageEnum.READ, MessageEnum.END]




if __name__ == '__main__':
    # p2 = multiprocessing.Process(target=preference_agent.read_msg)
    preference_agent = PreferenceAgent(child_conn)

    p1 = multiprocessing.Process(target=send_msgs, args=(parent_conn, msgs))
    p3 = multiprocessing.Process(target=recv_msg, args=(parent_conn,))
    p2 = multiprocessing.Process(target=preference_agent.read_msg)

    p1.start()
    p3.start()
    p2.start()

    p1.join()
    p2.join()
    p3.join()





