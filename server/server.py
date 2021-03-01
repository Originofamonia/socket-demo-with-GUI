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


class Command:
    command = ""
    payload = ""


class ServerThread(threading.Thread):
    # class of server thread
    def __init__(self, socket_instance,):
        threading.Thread.__init__(self)
        self.mySocket = socket_instance
        self.username = None

    def run(self):
        try:
            while True:
                print("Reading initial length")
                a = self.mySocket.recv(4)
                print("Wanted 4 bytes got " + str(len(a)) + " bytes")

                if len(a) < 4:
                    raise Exception("client closed socket, ending client thread")

                message_length = struct.unpack('i', a)[0]
                print("Message Length: ", message_length)
                data = bytearray()
                while message_length > len(data):
                    data += self.mySocket.recv(message_length - len(data))

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
                    file = open(server_filename, 'wb')
                    file.write(new_command.payload)
                    file.close()
                    # add spell check here
                    self.spell_check(server_filename)

                    reply_command = Command()
                    reply_command.command = "Uploaded " + server_filename
                    server_file = open(server_filename, 'rb')
                    reply_command.payload = server_file.read()
                    server_file.close()

                else:
                    print("Unknown Command:", new_command.command.replace('_', ' '))
                    raise Exception("Unknown Command")

                packed_data = pickle.dumps(reply_command)  # Serialize the class to a binary array
                # Length of the message is just the length of the array
                self.mySocket.sendall(struct.pack("i", len(packed_data)))
                self.mySocket.sendall(packed_data)

        except Exception as e:
            print(e)
            print("\nClosing socket")
            self.mySocket.close()

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
        self.mySocket.sendall(struct.pack("i", len(packed_data)))
        self.mySocket.sendall(packed_data)
        # self.mySocket.close()

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


def main():
    host = "localhost"
    port = 8789

    connections = {}
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Listening...")

    while True:
        (clientSocket, address) = server_socket.accept()
        print("Got incoming connection")
        # make a new instance of our thread class to handle requests
        new_thread = ServerThread(clientSocket)
        new_thread.start()  # call run()
        if new_thread.username not in connections:  # check whether username exists
            connections[new_thread.username] = new_thread
        else:
            new_thread.close_thread()


if __name__ == '__main__':
    main()
