"""
name
id
"""
import socket
import threading
import struct
import pickle
import select
import os
import tkinter as tk
import time


class Command:
    """
    data struct used between client-server
    """
    command = ""
    payload = ""


class ServerThread(threading.Thread):
    # class of server thread
    def __init__(self, socket_instance, connections):
        threading.Thread.__init__(self)
        self.my_socket = socket_instance
        self.connections = connections

    def run(self):
        try:
            while True:
                print("Reading initial length")
                a = self.my_socket.recv(4)
                print("Wanted 4 bytes got " + str(len(a)) + " bytes")

                if len(a) < 4:
                    raise Exception("client closed socket, ending client thread")

                message_length = struct.unpack('i', a)[0]
                print("Message Length: ", message_length)
                data = bytearray()
                while message_length > len(data):
                    data += self.my_socket.recv(message_length - len(data))

                new_command = pickle.loads(data)
                print("\nCommand is: ", new_command.command.replace('_', ' '))

                client_command = new_command.command.split(" ")
                # Divide the command to recognize it, " " is the divider

                if client_command[0] == "Connect":
                    self.username = new_command.payload
                    reply_command = self.username_check()
                    if reply_command.command == 'conflict':  # check duplicate username
                        packed_data = pickle.dumps(reply_command)  # Serialize the class to a binary array
                        # Length of the message is just the length of the array
                        self.my_socket.sendall(struct.pack("i", len(packed_data)))
                        self.my_socket.sendall(packed_data)
                        self.my_socket.close()
                        break

                elif client_command[0] == "Upload":
                    filename = client_command[1].split('/')[-1]
                    server_filename = 'server_received_' + filename
                    file = open(server_filename, 'wb')  # wb means write bytes
                    file.write(new_command.payload)  # write bytes to file
                    file.close()  # close file handler
                    # add lexicon check here
                    self.spell_check(server_filename)

                    reply_command = Command()
                    reply_command.command = "Uploaded " + server_filename
                    server_file = open(server_filename, 'rb')
                    reply_command.payload = server_file.read()
                    server_file.close()

                elif client_command[0] == 'exit':
                    reply_command = Command()
                    reply_command.command = 'exit'
                    reply_command.payload = 'done'
                    packed_data = pickle.dumps(reply_command)  # Serialize the class to a binary array
                    # Length of the message is just the length of the array
                    self.my_socket.sendall(struct.pack("i", len(packed_data)))
                    self.my_socket.sendall(packed_data)
                    self.my_socket.close()
                    break
                else:
                    # handle unknown command
                    print("Unknown Command:", new_command.command.replace('_', ' '))
                    raise Exception("Unknown Command")

                packed_data = pickle.dumps(reply_command)  # Serialize the class to a binary array
                # Length of the message is just the length of the array
                self.my_socket.sendall(struct.pack("i", len(packed_data)))
                self.my_socket.sendall(packed_data)

        except Exception as e:
            print(e)
            print("\nClosing socket")
            self.my_socket.close()

    def spell_check(self, server_filename):
        """
        http://openbookproject.net/courses/python4fun/spellcheck.html
        :return:
        """
        correct_words = open("correct.words").readlines()
        correct_words = [word.strip() for word in correct_words]
        modified_lines = []
        f = open(server_filename)
        lines = list(f)
        f.close()
        for i, line in enumerate(lines):  # for each line
            line = line.strip()
            file_words = line.split()
            for j, txt_word in enumerate(file_words):  # for each word in a line
                if txt_word not in correct_words:
                    file_words[j] = f"[{txt_word}]"
            modified_lines.append(' '.join(file_words) + '\n')

        with open(server_filename, 'w') as f:
            f.writelines(modified_lines)  # write back the modified file

    def username_check(self):
        usernames = []
        reply_command = Command()
        reply_command.payload = self.username
        for cli_thread in self.connections:
            usernames.append(cli_thread.username)
        if self.username in usernames:
            reply_command.command = 'conflict'
        else:
            reply_command.command = "connected"

        return reply_command


class Server(threading.Thread):
    def __init__(self, host, port):
        super(Server, self).__init__()
        self.root = tk.Tk()
        self.root.title("Server status")
        self.root.geometry('250x250')
        self.frm = tk.Frame(self.root,)
        self.connections = []  # list holds client connections
        self.host = host
        self.port = port

        # GUI
        self.frm_m = tk.Frame(self.frm,)
        self.var = tk.StringVar()
        self.label = tk.Label(self.root, textvariable=self.var, relief=tk.RAISED)
        self.var.set('Connected usernames')
        self.scrollbar = tk.Scrollbar(master=self.frm_m)
        self.listbox = tk.Listbox(master=self.frm_m, yscrollcommand=self.scrollbar.set,)
        tk.Button(self.frm_m, text='Refresh', command=self.refresh, width=15).pack(side=tk.BOTTOM)
        tk.Button(self.frm_m, text='Exit', command=self.exit, width=15).pack(side=tk.BOTTOM)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.label.pack()
        self.frm_m.pack()
        self.frm.pack()

    def run(self):
        """
        https://pymotw.com/2/select/#poll
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)  # if 1, will have multi client problem
        print("Listening...")

        while True:
            (client_socket, address) = self.server_socket.accept()  # server socket accepting client connection
            print("Incoming connection ",)
            # make a new instance of our thread class to handle requests
            new_thread = ServerThread(client_socket, self.connections)
            new_thread.start()  # call run()
            time.sleep(0.09)  # control thread execution order

            self.connections.append(new_thread)

            # update listbox showing connected usernames
            self.listbox.delete(0, tk.END)  # clear all in listbox
            for x in self.connections:
                self.listbox.insert(tk.END, x.username)  # insert new data

    def refresh(self,):
        # check username in server, not server_thread
        # 2. update listbox
        for cli_thread in self.connections:
            if cli_thread.my_socket.fileno() == -1:
                self.connections.remove(cli_thread)
        self.listbox.delete(0, tk.END)  # clear all
        for x in self.connections:
            self.listbox.insert(tk.END, x.username)  # insert new data

    def check_username(self, new_thread):
        # check username conflict
        usernames = []
        for cli_thread in self.connections:
            usernames.append(cli_thread.username)
        if new_thread.username in usernames:
            reply_command = Command()
            reply_command.command = 'conflict'
            reply_command.payload = new_thread.username
            packed_data = pickle.dumps(reply_command)  # Serialize the class to a binary array
            # Length of the message is just the length of the array
            new_thread.my_socket.sendall(struct.pack("i", len(packed_data)))
            new_thread.my_socket.sendall(packed_data)
            new_thread.my_socket.close()
            del new_thread
        else:
            self.connections.append(new_thread)

    def exit(self):
        try:
            self.server_socket.close()
            os._exit(0)

        except Exception as ex:
            print('error in exit: ', ex)


def main():
    host = "localhost"
    port = 7789

    server = Server(host, port)
    server.start()
    server.root.mainloop()


if __name__ == '__main__':
    main()
