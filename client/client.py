"""
name
id
"""
import socket
import struct
import pickle
import string
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename


class Command:
    """
    Used for socket transmission
    """
    command = ""
    payload = ""


class Application:
    # class for client GUI
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.root = tk.Tk()
        self.root.title("File transfer")
        self.frm = tk.Frame(self.root)
        self.sock = None

        # Mid
        self.frm_M = tk.Frame(self.frm)
        self.scrollbar = tk.Scrollbar(master=self.frm_M)
        self.listbox = tk.Listbox(
            master=self.frm_M,
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        text_input = tk.Entry(master=self.frm_M)
        text_input.pack(expand=True)
        text_input.bind("<Return>", lambda x: self.connect(text_input))
        # text_input.insert(0, "username")
        tk.Button(self.frm_M, text='Connect', command=lambda: self.connect(text_input), width=15).pack(side=tk.TOP)
        tk.Button(self.frm_M, text='Upload', command=self.upload, width=15).pack(side=tk.TOP)
        self.frm_M.pack(side=tk.LEFT)

        self.frm.pack()

    def connect(self, text_input):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        msg = text_input.get()
        text_input.delete(0, tk.END)
        try:
            add_command = Command()
            add_command.command = f'Connect {msg}'
            add_command.payload = msg
            packed_data = pickle.dumps(add_command)
            self.sock.sendall(struct.pack('i', len(packed_data)))
            self.sock.sendall(packed_data)

            reply_len = struct.unpack("i", self.sock.recv(4))[0]
            data = bytearray()
            while reply_len > len(data):
                data += self.sock.recv(reply_len - len(data))
            reply_command = pickle.loads(data)  # Receive the server reply

            server_command = reply_command.command.split(" ")
            if server_command[0] == "Connect":
                username = reply_command.payload
                if not username:
                    self.listbox.insert(1, f"username: {username} existed")
                    self.sock.close()
                else:
                    self.listbox.insert(1, f'{username} connected')

        except Exception as e:
            print('Error occurred: ', e)

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
                self.listbox.insert(2, "Echoed server file: ", server_filename)
                server_file = open(server_filename, 'wb')
                server_file.write(reply_command.payload)
                server_file.close()
                return server_filename

        except Exception as e:
            print("Error occurred: ", e)


def main():
    host = "localhost"
    port = 8789

    root = Application(host, port)
    tk.mainloop()

    root.sock.close()


if __name__ == '__main__':
    main()
