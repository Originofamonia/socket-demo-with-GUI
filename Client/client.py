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
    command = ""
    payload = ""


# 1.Adding Songs (and return SongID)
# def add_song(song_name, s):
#     # send file from client to server
#     try:
#         add_command = Command()
#         add_command.command = "AddSong" + " " + song_name.replace(' ', '_')
#         # because ' ' is a divider
#         music = open("Song/" + song_name + ".mp3", 'rb')
#         add_command.payload = music.read()
#         music.close()  # Set Command and Payload
#
#         packed_data = pickle.dumps(add_command)
#         s.sendall(struct.pack("i", len(packed_data)))
#         s.sendall(packed_data)  # Send Binary data
#
#         reply_len = struct.unpack("i", s.recv(4))[0]
#         data = bytearray()
#         while reply_len > len(data):
#             data += s.recv(reply_len - len(data))
#         reply_command = pickle.loads(data)  # Receive the server reply
#
#         server_command = reply_command.command.split(" ")
#         if server_command[0] == "SongAdded":
#             SongID = server_command[1]
#             print("The song was successfully added as ID:", SongID)
#             return SongID
#     except Exception as e:
#         print("Error occured: ", e)


# 2.Creating a playlist:
# def create_list(listName, s):
#     try:
#         addCommand = Command()
#         addCommand.command = "CreatePlayList" + " " + listName.replace(' ', '_')
#         # because ' ' is a divider
#
#         packedData = pickle.dumps(addCommand)
#         s.sendall(struct.pack("i", len(packedData)))
#         s.sendall(packedData)  # Send Binary data
#
#         replyLen = struct.unpack("i", s.recv(4))[0]
#         data = bytearray()
#         while replyLen > len(data):
#             data += s.recv(replyLen - len(data))
#         replyCommand = pickle.loads(data)  # Receive the server reply
#
#         ServerCommand = replyCommand.command.split(" ")
#         if ServerCommand[0] == "PlayListCreated":
#             listID = ServerCommand[1]
#             playlist = open("Lists/" + listID + ".txt", 'w')
#             playlist.write(listName + "\n")
#             playlist.close()  # Create a new playlist at Client terminal
#             print("The playlist was successfully created as ID:", listID)
#             return listID
#     except Exception as e:
#         print("Error occured: ", e)


# 3.Download a list of playlists available:
# def getPlayLists(s):
#     try:
#         getCommand = Command()
#         getCommand.command = "GetAllPlayLists"
#         # because ' ' is a divider
#
#         packedData = pickle.dumps(getCommand)
#         s.sendall(struct.pack("i", len(packedData)))
#         s.sendall(packedData)  # Send Binary data
#
#         replyLen = struct.unpack("i", s.recv(4))[0]
#         data = bytearray()
#         while replyLen > len(data):
#             data += s.recv(replyLen - len(data))
#         replyCommand = pickle.loads(data)  # Receive the server reply
#
#         if replyCommand.command == "AllPlayList":
#             print("Playlists is:", replyCommand.payload)
#             return replyCommand.payload
#     except Exception as e:
#         print("Error occured: ", e)


# 4.Download a PlayList: (and save it as <PlayListID>.txt)
# def getPlayList(playlistID, s):
#     try:
#         getCommand = Command()
#         getCommand.command = "GetPlayList" + " " + str(playlistID)  # " " is a divider
#         packedData = pickle.dumps(getCommand)
#         totalLen = len(packedData)
#
#         s.sendall(struct.pack("i", totalLen))
#         s.sendall(packedData)
#
#         replyLen = struct.unpack("i", s.recv(4))[0]
#         data = bytearray()
#         while replyLen > len(data):
#             data += s.recv(replyLen - len(data))
#
#         replyCommand = pickle.loads(data)
#         f = open("Lists/" + str(playlistID) + ".txt", "wb")
#         f.write(replyCommand.payload)
#         print("PlayList saved as " + str(playlistID) + ".txt")
#         f.close()
#     except Exception as e:
#         print("Error occured: ", e)


# 5.Download a song by songID: (and save it as songName.mp3)
# def getSongByID(songID, songName, s):
#     try:
#         getCommand = Command()
#         getCommand.command = "GetSong" + " " + str(songID)  # " " is a divider
#         packedData = pickle.dumps(getCommand)
#         totalLen = len(packedData)
#
#         s.sendall(struct.pack("i", totalLen))
#         s.sendall(packedData)
#
#         replyLen = struct.unpack("i", s.recv(4))[0]
#         data = bytearray()
#         while replyLen > len(data):
#             data += s.recv(replyLen - len(data))
#
#         replyCommand = pickle.loads(data)
#         f = open("Song/" + songName + ".mp3", "wb")
#         f.write(replyCommand.payload)
#         print("Song saved as " + songName + ".mp3")
#         f.close()
#     except Exception as e:
#         print("Error occured: ", e)


# 6.Add/remove songs from a playlist: (option is for Add/remove model)
# def EditSong(songID, listID, option, s):
#     try:
#         editCommand = Command()
#         if option == "add":
#             editCommand.command = "AddSongToList " + str(songID) + " " + str(listID)
#         elif option == "remove":
#             editCommand.command = "RemoveSongFromList " + str(songID) + " " + str(listID)
#         else:
#             raise Exception("No model selected")
#
#         packedData = pickle.dumps(editCommand)
#         s.sendall(struct.pack("i", len(packedData)))
#         s.sendall(packedData)  # Send Binary data
#
#         replyLen = struct.unpack("i", s.recv(4))[0]
#         data = bytearray()
#         while replyLen > len(data):
#             data += s.recv(replyLen - len(data))
#         replyCommand = pickle.loads(data)  # Receive the server reply
#
#         if replyCommand.command == "SongAdded":
#             print("The song(ID:" + str(songID) +
#                   ") is successfully added to the playlist(ID:" + str(listID) + ").")
#         elif replyCommand.command == "SongRemoved":
#             print("The song is successfully removed")
#         # getPlayList(listID, s) # Refresh the playlist data
#     except Exception as e:
#         print("Error occured: ", e)


# 9.Remove a song from the server:
# def removeSong(songID, s):
#     try:
#         removeCommand = Command()
#         removeCommand.command = "RemoveSong" + " " + str(songID)  # " " is a divider
#         packedData = pickle.dumps(removeCommand)
#         totalLen = len(packedData)
#
#         s.sendall(struct.pack("i", totalLen))
#         s.sendall(packedData)
#
#         replyLen = struct.unpack("i", s.recv(4))[0]
#         data = bytearray()
#         while replyLen > len(data):
#             data += s.recv(replyLen - len(data))
#
#         replyCommand = pickle.loads(data)
#         if replyCommand.command == "SongRemovedOK":
#             print("The song(ID: " + str(songID)
#                   + ") is successfully removed from sever.")
#     except Exception as e:
#         print("Error occurred: ", e)


# Get a list of all available song
# def getSongList(s):
#     getCommand = Command()
#     getCommand.command = "GetSongList"
#     packedData = pickle.dumps(getCommand)
#     totalLen = len(packedData)
#
#     s.sendall(struct.pack("i", totalLen))
#     s.sendall(packedData)
#
#     msg = s.recv(4)
#     replyLen = struct.unpack("i", msg)[0]
#     data = bytearray()
#     while replyLen > len(data):
#         data += s.recv(replyLen - len(data))
#     replyCommand = pickle.loads(data)
#
#     print("SongList is: ", replyCommand.payload)
#     return replyCommand.payload


# Class for GUI
class Application:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.root = tk.Tk()
        self.root.title("File transfer")
        self.frm = tk.Frame(self.root)
        self.sock = None

        # Left
        # self.frm_L = tk.Frame(self.frm)
        #
        # tk.Label(self.frm_L, text=' ').pack()
        # tk.Label(self.frm_L, text='Local Song',
        #          font=('Arial', 10)).pack()
        #
        # self.localsong_var = tk.StringVar()
        # self.localsong = tk.Listbox(self.frm_L, width=20, height=10,
        #                             listvariable=self.localsong_var)
        # for a, b, files in os.walk("Song/"):
        #     for item in files:
        #         self.localsong.insert(tk.END, item)
        # self.localsong.pack()
        #
        # tk.Button(self.frm_L, text="Show Available PlayLists",
        #           command=self.showallplaylists, width=20).pack()
        # tk.Label(self.frm_L, text='Available PlayLists',
        #          font=('Arial', 10)).pack()
        #
        # self.playLists_var = tk.StringVar()
        # self.playLists = tk.Listbox(self.frm_L, width=20,
        #                             height=10, listvariable=self.playLists_var)
        #
        # tk.Button(self.frm_L, text="Create PlayList",
        #           command=self.createlist, width=15).pack(side=tk.BOTTOM)
        #
        # self.frm_LB = tk.Frame(self.frm_L)
        # tk.Label(self.frm_LB, text='ListName:', font=('Arial', 10), height=1).pack(side=tk.LEFT)
        # self.newlistname = tk.StringVar()
        # tk.Entry(self.frm_LB, textvariable=self.newlistname,
        #          width=10, font=('Arial', 10)).pack(side=tk.RIGHT)
        # self.frm_LB.pack(side=tk.BOTTOM)
        #
        # self.playLists.pack()
        # self.frm_L.pack(side=tk.LEFT)

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
        # tk.Button(self.frm_M, text="Add Song >>",
        #           command=self.addsong, width=15).pack(side=tk.TOP)
        # tk.Button(self.frm_M, text="<< Get Song",
        #           command=self.getsong, width=15).pack(side=tk.TOP)
        # add upload button
        tk.Button(self.frm_M, text='Upload', command=self.upload, width=15).pack(side=tk.TOP)
        # tk.Label(self.frm_M, text='\n\n\n\n\n\n\n\n\n\n').pack(side=tk.TOP)
        # tk.Button(self.frm_M, text="Get PlayList >>",
        #           command=self.getplaylist, width=15).pack(side=tk.TOP)
        self.frm_M.pack(side=tk.LEFT)

        # Right
        # self.frm_R = tk.Frame(self.frm)
        # tk.Button(self.frm_R, text="Remove ↓ From Server",
        #           command=self.removesong, width=18).pack(side=tk.TOP)
        # tk.Label(self.frm_R, text='Sever Song',
        #          font=('Arial', 10)).pack()
        #
        # self.hostsong_var = tk.StringVar()
        # self.hostsong = tk.Listbox(self.frm_R, width=20,
        #                            height=10, listvariable=self.hostsong_var)
        # self.hostsongList = getSongList(self.sock)
        # # Get all avaliable songs at start
        # for item in self.hostsongList:
        #     self.thelist = str(item) + ". " + self.hostsongList[item] + ".mp3"
        #     self.hostsong.insert(tk.END, self.thelist)
        # self.hostsong.pack()
        #
        # tk.Button(self.frm_R, text="↓ Add to playlist",
        #           command=self.addsongtolist, width=15, height=1).pack()
        #
        # self.listname = tk.Label(self.frm_R, font=('Arial', 10))
        # self.listname["text"] = "Songs in PlayList"
        # self.listname.pack()
        # self.frm_R.pack()
        #
        # self.songList_var = tk.StringVar()
        # self.songList = tk.Listbox(self.frm_R, width=20,
        #                            height=10, listvariable=self.songList_var)
        #
        # self.frm_RB = tk.Frame(self.frm_R)
        # tk.Button(self.frm_RB, text="Remove Song",
        #           command=self.removelistsong, width=15).pack()
        # tk.Label(self.frm_RB, text=' ').pack()
        # self.frm_RB.pack(side=tk.BOTTOM)
        #
        # self.songList.pack()
        # self.frm_R.pack(side=tk.RIGHT)

        self.frm.pack()

    def connect(self, text_input):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        msg = text_input.get()
        print(msg)
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

    # def addsong(self):
    #     songName = self.localsong.get(self.localsong.curselection())
    #     songName = songName.replace(".mp3", "")
    #     songID = add_song(songName, self.sock)  # Function 1 Called
    #     self.hostsong.insert(tk.END, songID + ". " + songName + ".mp3")

    # def getsong(self):
    #     Song = self.hostsong.get(self.hostsong.curselection())
    #     songID = int(Song.split(". ")[0])
    #     songName = Song.split(". ")[1].replace(".mp3", "")
    #     count = 0
    #     localsong = self.localsong_var.get().split(", ")
    #     for item in localsong:
    #         if songName in localsong[count]:
    #             print("The song is exist in local song")
    #             return
    #         count = count + 1
    #     getSongByID(songID, songName, self.sock)  # Function 5 Called
    #     self.localsong.insert(tk.END, songName + ".mp3")

    # def removesong(self):
    #     Song = self.hostsong.get(self.hostsong.curselection())
    #     songID = int(Song.split(". ")[0])
    #     count = 0
    #     hostsong = self.hostsong_var.get().split(", ")
    #     for item in hostsong:
    #         if str(songID) + ". " in hostsong[count]:
    #             self.hostsong.delete(count)
    #         count = count + 1
    #     count = 0
    #     songlist = self.songList_var.get().split(", ")
    #     for item in songlist:
    #         if str(songID) + ". " in songlist[count]:
    #             self.songList.delete(count)
    #         count = count + 1
    #     removeSong(songID, self.sock)  # Function 9 Called

    # def getplaylist(self):
    #     self.songList_var.set('')
    #     play_list = self.playLists.get(self.playLists.curselection())
    #     list_id = int(play_list.split(". ")[0])
    #     getPlayList(list_id, self.sock)  # Function 4 Called
    #     f = open("Lists/" + str(list_id) + ".txt", "r")
    #     flag = 0
    #     for line in f:
    #         if flag == 0:
    #             self.listname["text"] = str(list_id) + ". " + line.replace("\n", "")
    #             self.listname.pack()
    #             self.frm_R.pack()
    #             flag = 1
    #         else:
    #             read = line.split(",")
    #             self.songList.insert(tk.END, read[0] + ". "
    #                                  + read[1].replace("\n", "") + ".mp3")
    #     f.close()

    # def createlist(self):
    #     list_name = self.newlistname.get()
    #     list_id = create_list(list_name, self.sock)  # Function 2 Called
    #     self.playLists.insert(tk.END, list_id + ". " + list_name)

    # def addsongtolist(self):
    #     try:  # Avoid choosing a wrong item before pressing button
    #         song = self.hostsong.get(self.hostsong.curselection())
    #         song_id = int(song.split(". ")[0])
    #         song_name = song.split(". ")[1]
    #         if self.listname["text"] == 'Songs in PlayList':
    #             print("Please choose(get) one playlist at first")
    #         else:
    #             count = 0
    #             songlist = self.songList_var.get().split(", ")
    #             for item in songlist:
    #                 if str(song_id) + ". " in songlist[count]:
    #                     print("Song already exist in the list")
    #                     return
    #                 count = count + 1
    #             listID = int(self.listname["text"].split(". ")[0])
    #             self.songList.insert(tk.END, str(song_id) + ". " + song_name)
    #             EditSong(song_id, listID, "add", self.sock)  # Function 6 Called
    #     except Exception as e:
    #         print(e)
    #         return

    # def removelistsong(self):
    #     Song = self.songList.get(self.songList.curselection())
    #     songID = int(Song.split(". ")[0])
    #     count = 0
    #     songlist = self.songList_var.get().split(", ")
    #     for item in songlist:
    #         if str(songID) + ". " in songlist[count]:
    #             self.songList.delete(count)
    #         count = count + 1
    #     listID = int(self.listname["text"].split(". ")[0])
    #     EditSong(songID, listID, "remove", self.sock)  # Function 6 Called

    # def showallplaylists(self):
    #     self.theplaylist = getPlayLists(self.sock)  # Function 3 Called
    #     # Get all available playlists at start
    #     for item in self.theplaylist:
    #         self.thelist = str(item) + ". " + self.theplaylist[item]
    #         self.playLists.insert(tk.END, self.thelist)


def main():
    host = "localhost"
    port = 6789

    root = Application(host, port)
    tk.mainloop()

    root.sock.close()


if __name__ == '__main__':
    main()
