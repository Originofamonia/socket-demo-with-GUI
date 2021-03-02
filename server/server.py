"""
name
id
"""
import socket
import threading
import struct
import pickle
import string
import os
import tkinter as tk


class Command:
    """
    data struct used between client-server
    """
    command = ""
    payload = ""


class ServerThread(threading.Thread):
    # class of server thread
    def __init__(self, socket_instance,):
        threading.Thread.__init__(self)
        self.my_socket = socket_instance
        self.username = None
        # self.connections = {}

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
                    reply_command = Command()
                    reply_command.command = "Connect checking"
                    reply_command.payload = self.username

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
                    return "exit"
                else:
                    print("Unknown Command:", new_command.command.replace('_', ' '))
                    raise Exception("Unknown Command")

                packed_data = pickle.dumps(reply_command)  # Serialize the class to a binary array
                # Length of the message is just the length of the array
                self.my_socket.sendall(struct.pack("i", len(packed_data)))
                self.my_socket.sendall(packed_data)
                return 0

        except Exception as e:
            print(e)
            print("\nClosing socket")
            self.my_socket.close()

    def close_thread(self):
        """
        When username already existed, close this thread.
        :return:
        """
        reply_command = Command()
        reply_command.command = "Connect checking"
        reply_command.payload = str()
        packed_data = pickle.dumps(reply_command)  # Serialize the class to a binary array
        # Length of the message is just the length of the array
        self.my_socket.sendall(struct.pack("i", len(packed_data)))
        self.my_socket.sendall(packed_data)
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
            f.writelines(modified_lines)
            # for item in modified_lines:
            #     f.write("%s" % item)


class Server(threading.Thread):
    def __init__(self, host, port):
        super(Server, self).__init__()

        self.root = tk.Tk()
        self.root.title("Server status")
        self.root.geometry('250x250')
        self.frm = tk.Frame(self.root,)
        self.connections = {}
        self.host = host
        self.port = port

        # GUI
        self.frm_m = tk.Frame(self.frm,)
        self.var = tk.StringVar()
        self.label = tk.Label(self.root, textvariable=self.var, relief=tk.RAISED)
        self.var.set('Connected usernames')
        self.scrollbar = tk.Scrollbar(master=self.frm_m)
        self.listbox = tk.Listbox(master=self.frm_m, yscrollcommand=self.scrollbar.set,)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.label.pack()
        self.frm_m.pack()
        self.frm.pack()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)  # if 1, will have multi client problem
        print("Listening...")

        while True:
            for name, cli_thread in self.connections.items():
                if cli_thread.my_socket.fileno() == -1:
                    self.connections.pop(name, None)
            (client_socket, address) = server_socket.accept()
            print("Got incoming connection")
            # make a new instance of our thread class to handle requests
            new_thread = ServerThread(client_socket)
            new_thread.start()  # call run()
            if new_thread.username not in self.connections:  # check whether username exists
                self.connections[new_thread.username] = new_thread
            else:
                new_thread.close_thread()

            # update listbox showing connected usernames
            self.listbox.delete(0, tk.END)  # clear all
            self.listbox.insert(tk.END, list(self.connections.keys()))  # insert new data


def main():
    host = "localhost"
    port = 7789

    server = Server(host, port)
    server.start()
    server.root.mainloop()
    # connections = {}
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind((host, port))
    # server_socket.listen(1)
    #
    # print("Listening...")
    #
    # while True:
    #     (clientSocket, address) = server_socket.accept()
    #     print("Got incoming connection")
    #     # make a new instance of our thread class to handle requests
    #     new_thread = ServerThread(clientSocket)
    #     new_thread.start()  # call run()
    #     if new_thread.username not in connections:  # check whether username exists
    #         connections[new_thread.username] = new_thread
    #     else:
    #         new_thread.close_thread()


if __name__ == '__main__':
    main()
