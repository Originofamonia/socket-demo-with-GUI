"""
Project 2
name
id
"""
import socket
import struct
import pickle
import select
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
import threading
from queue import Queue
import time


class Command:
    """
    Used for socket transmission
    """
    command = ""
    payload = ""


class Application:
    # class for client GUI
    def __init__(self, host, port):
        # super(Application, self).__init__()
        self.host = host
        self.port = port
        self.root = tk.Tk()
        self.root.title("File transfer")
        self.frm = tk.Frame(self.root)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.lexicon_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.q = Queue()
        # Mid
        self.frm_M = tk.Frame(self.frm)
        self.scrollbar = tk.Scrollbar(master=self.frm_M)
        self.listbox = tk.Listbox(
            master=self.frm_M,
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.username_entry = tk.Entry(master=self.frm_M)
        self.username_entry.pack(expand=True)
        self.username_entry.bind("<Return>", lambda x: self.connect(self.username_entry))
        self.lexicon_entry = tk.Entry(master=self.frm_M)
        self.lexicon_entry.pack(expand=True)
        self.lexicon_entry.bind("<Return>", lambda x: self.add_lexicon(self.lexicon_entry))
        tk.Button(self.frm_M, text='Connect', command=lambda: self.connect(self.username_entry),
                  width=15).pack(side=tk.TOP)
        tk.Button(self.frm_M, text='Add lexicon', command=lambda: self.add_lexicon(self.lexicon_entry),
                  width=15).pack(side=tk.TOP)
        tk.Button(self.frm_M, text='Upload', command=self.upload, width=15).pack(side=tk.TOP)
        tk.Button(self.frm_M, text='Exit', command=self.exit, width=15).pack(side=tk.TOP)
        self.frm_M.pack(side=tk.LEFT)

        self.frm.pack()

    def connect(self, text_input):
        self.username = text_input.get()
        text_input.delete(0, tk.END)
        th = threading.Thread(target=self.connect2,)
        th.start()
        # time.sleep(0.01)
        self.sock.connect((self.host, self.port))
        try:
            add_command = Command()
            add_command.command = f'Connect {self.username}'
            add_command.payload = self.username
            packed_data = pickle.dumps(add_command)
            self.sock.sendall(struct.pack('i', len(packed_data)))
            self.sock.sendall(packed_data)

            reply_len = struct.unpack("i", self.sock.recv(4))[0]
            data = bytearray()
            while reply_len > len(data):
                data += self.sock.recv(reply_len - len(data))
            reply_command = pickle.loads(data)  # Receive the server reply
            server_command = reply_command.command.split(" ")
            if server_command[0] == "connected":
                username = reply_command.payload
                self.listbox.delete(0, tk.END)
                self.listbox.insert(1, f'{username} connected')
            elif server_command[0] == 'conflict':
                username = reply_command.payload
                self.listbox.delete(0, tk.END)
                self.listbox.insert(1, f'{username} conflicted')

        except Exception as e:
            print('Error in connect: ', e)

    def connect2(self,):
        self.lexicon_sock.connect((self.host, self.port))
        try:
            add_command = Command()
            add_command.command = f'Connect {self.username}_lex'
            add_command.payload = self.username + '_lex'
            packed_data = pickle.dumps(add_command)
            self.lexicon_sock.sendall(struct.pack('i', len(packed_data)))
            self.lexicon_sock.sendall(packed_data)

            reply_len = struct.unpack("i", self.lexicon_sock.recv(4))[0]
            data = bytearray()
            while reply_len > len(data):
                data += self.lexicon_sock.recv(reply_len - len(data))
            reply_command = pickle.loads(data)  # Receive the server reply
            server_command = reply_command.command.split(" ")
            print('connect2: ', server_command)

        except Exception as e:
            print('Error in connect: ', e)

        self.wait_poll_th = threading.Thread(target=self.wait_poll, )
        self.wait_poll_th.start()

    def add_lexicon(self, lexicon_entry):
        lexicon = lexicon_entry.get()
        lexicon_entry.delete(0, tk.END)
        self.q.put(lexicon)
        self.listbox.insert(tk.END, f'queue add: {lexicon}')

    def wait_poll(self):
        try:
            while True:
                a = self.lexicon_sock.recv(4)
                print("Wanted 4 bytes got " + str(len(a)) + " bytes")

                if len(a) < 4:
                    raise Exception("client closed socket, ending client thread")

                message_length = struct.unpack('i', a)[0]
                print("Message Length: ", message_length)
                data = bytearray()
                while message_length > len(data):
                    data += self.lexicon_sock.recv(message_length - len(data))

                new_command = pickle.loads(data)
                print("\nCommand is: ", new_command.command.replace('_', ' '))
                server_command = new_command.command.split(" ")
                # Divide the command to recognize it, " " is the divider
                reply_command = Command()

                if server_command[0] == "poll":
                    reply_command.command = 'addlexicon'
                    if self.q.empty():
                        reply_command.payload = ''
                    else:
                        reply_command.payload = ' '.join(list(self.q.queue))
                        self.q.queue.clear()

                    self.listbox.delete(1, tk.END)
                    self.listbox.insert(tk.END, f'polled queue: {reply_command.payload}')

                elif server_command[0] == 'addlexicon':
                    print("server_command[0] == 'addlexicon'")
                    continue
                else:
                    # handle unknown command
                    print("Unknown Command2:", new_command.command.replace('_', ' '))
                    raise Exception("Unknown Command")

                packed_data = pickle.dumps(reply_command)  # Serialize the class to a binary array
                # Length of the message is just the length of the array
                self.lexicon_sock.sendall(struct.pack("i", len(packed_data)))
                self.lexicon_sock.sendall(packed_data)
                print('sent queue')

        except Exception as e:
            print(e)
            print("\nClosing socket")
            self.lexicon_sock.close()

    def upload(self):
        try:
            filename = askopenfilename()
            add_command = Command()
            add_command.command = f"Upload {filename.replace(' ', '_')}"
            file = open(filename, 'rb')
            add_command.payload = file.read()
            file.close()

            packed_data = pickle.dumps(add_command)
            self.sock.sendall(struct.pack("i", len(packed_data)))
            self.sock.sendall(packed_data)

            reply_len = struct.unpack("i", self.sock.recv(4))[0]
            data = bytearray()
            while reply_len > len(data):
                data += self.sock.recv(reply_len - len(data))
            reply_command = pickle.loads(data)  # Receive the server reply

            server_command = reply_command.command.split(" ")
            if server_command[0] == "Uploaded":
                server_filename = server_command[1]
                self.listbox.insert(2, "Server echoed file: ", server_filename)
                server_file = open(server_filename, 'wb')
                server_file.write(reply_command.payload)
                server_file.close()
                return server_filename

        except Exception as e:
            print("Error in upload: ", e)

    def exit(self):
        try:
            # send exit message
            add_command = Command()
            add_command.command = 'exit'
            add_command.payload = self.username
            packed_data = pickle.dumps(add_command)
            self.sock.sendall(struct.pack('i', len(packed_data)))
            self.sock.sendall(packed_data)

            reply_len = struct.unpack("i", self.sock.recv(4))[0]
            data = bytearray()
            while reply_len > len(data):
                data += self.sock.recv(reply_len - len(data))
            reply_command = pickle.loads(data)  # Receive the server reply
            self.listbox.insert(3, "server echoed: ", reply_command.payload)
            # kill itself
            self.sock.close()
            self.lexicon_sock.close()
            os._exit(0)

        except Exception as ex:
            print('error in exit: ', ex)


def main():
    host = "localhost"
    port = 7789

    app = Application(host, port)
    # app.start()
    app.root.mainloop()

    app.sock.close()


if __name__ == '__main__':
    main()
