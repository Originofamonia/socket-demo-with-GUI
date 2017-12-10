import socket
import struct
import pickle
import string
import os
from tkinter import *
#import playsound


host = "localhost"
port = 4567

class Command:
    command = ""
    payload = ""

# 1.Adding Songs (and return SongID)
def addSong(songName, s):
    try:
        addCommand = Command()
        addCommand.command = "AddSong" + " " + songName.replace(' ','_')
        # because ' ' is a divider
        music = open("Song/" + songName + ".mp3", 'rb')
        addCommand.payload = music.read()
        music.close() # Set Command and Payload
        
        packedData = pickle.dumps(addCommand)
        s.sendall(struct.pack("i", len(packedData)))
        s.sendall(packedData) # Send Binary data

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))
        replyCommand = pickle.loads(data) # Receive the server reply
        
        ServerCommand = replyCommand.command.split(" ")
        if ServerCommand[0] == "SongAdded":
            SongID = ServerCommand[1]
            print("The song was successfully added as ID:", SongID)
            return SongID
    except Exception as e:
        print("Error occured: ", e)

# 2.Creating a playlist:
def createList(listName, s):
    try:
        addCommand = Command()
        addCommand.command = "CreatePlayList" + " " + listName.replace(' ','_')
        # because ' ' is a divider
        
        packedData = pickle.dumps(addCommand)
        s.sendall(struct.pack("i", len(packedData)))
        s.sendall(packedData) # Send Binary data

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))
        replyCommand = pickle.loads(data) # Receive the server reply
        
        ServerCommand = replyCommand.command.split(" ")
        if ServerCommand[0] == "PlayListCreated":
            listID = ServerCommand[1]
            playlist = open("Lists/" + listID + ".txt", 'w')
            playlist.write(listName + "\n")
            playlist.close() # Create a new playlist at Client terminal
            print("The playlist was successfully created as ID:", listID)
            return listID
    except Exception as e:
        print("Error occured: ", e)

# 3.Download a list of playlists available:
def getPlayLists(s):
    try:
        getCommand = Command()
        getCommand.command = "GetAllPlayLists"
        # because ' ' is a divider
        
        packedData = pickle.dumps(getCommand)
        s.sendall(struct.pack("i", len(packedData)))
        s.sendall(packedData) # Send Binary data

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))
        replyCommand = pickle.loads(data) # Receive the server reply
        
        if replyCommand.command == "AllPlayList":
            print("Playlists is:", replyCommand.payload)
            return replyCommand.payload
    except Exception as e:
        print("Error occured: ", e)

# 4.Download a PlayList: (and save it as <PlayListID>.txt)
def getPlayList(playlistID, s):
    try:
        getCommand = Command()
        getCommand.command = "GetPlayList" + " " + str(playlistID) # " " is a divider
        packedData = pickle.dumps(getCommand)
        totalLen = len(packedData)

        s.sendall(struct.pack("i", totalLen))
        s.sendall(packedData)

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))

        replyCommand = pickle.loads(data)
        f = open("Lists/" + str(playlistID) + ".txt", "wb")
        f.write(replyCommand.payload)
        print("PlayList saved as " + str(playlistID) + ".txt")
        f.close()
    except Exception as e:
        print("Error occured: ", e)

# 5.Download a song by songID: (and save it as songName.mp3)
def getSongByID(songID, songName, s):
    try:
        getCommand = Command()
        getCommand.command = "GetSong" + " " + str(songID) # " " is a divider
        packedData = pickle.dumps(getCommand)
        totalLen = len(packedData)

        s.sendall(struct.pack("i", totalLen))
        s.sendall(packedData)

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))

        replyCommand = pickle.loads(data)
        f = open("Song/" + songName + ".mp3", "wb")
        f.write(replyCommand.payload)
        print("Song saved as " + songName + ".mp3")
        f.close()
    except Exception as e:
        print("Error occured: ", e)

# 6.Add/remove songs from a playlist: (option is for Add/remove model)
def EditSong(songID, listID, option, s):
    try:
        editCommand = Command()
        if option == "add":
            editCommand.command = "AddSongToList " + str(songID) + " " + str(listID)
        elif option == "remove":
            editCommand.command = "RemoveSongFromList " + str(songID) + " " + str(listID)
        else:
            raise Exception("No model selected")
        
        packedData = pickle.dumps(editCommand)
        s.sendall(struct.pack("i", len(packedData)))
        s.sendall(packedData) # Send Binary data

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))
        replyCommand = pickle.loads(data) # Receive the server reply
        
        if replyCommand.command == "SongAdded":
            print ("The song(ID:" + str(songID) +
                   ") is successfully added to the playlist(ID:" + str(listID) + ").")
        elif replyCommand.command == "SongRemoved":
            print ("The song is successfully removed")
        #getPlayList(listID, s) # Refresh the playlist data
    except Exception as e:
        print("Error occured: ", e)

# 9.Remove a song from the server:
def removeSong(songID, s):
    try:
        removeCommand = Command()
        removeCommand.command = "RemoveSong" + " " + str(songID) # " " is a divider
        packedData = pickle.dumps(removeCommand)
        totalLen = len(packedData)

        s.sendall(struct.pack("i", totalLen))
        s.sendall(packedData)

        replyLen = struct.unpack("i", s.recv(4))[0]
        data = bytearray()
        while (replyLen > len(data)):
            data += s.recv(replyLen - len(data))

        replyCommand = pickle.loads(data)
        if replyCommand.command == "SongRemovedOK":
            print("The song(ID: " + str(songID)
                  + ") is successfully removed from sever.")
    except Exception as e:
        print("Error occured: ", e)

# Get a list of all avaliable song
def getSongList(s):
    getCommand = Command()
    getCommand.command = "GetSongList"
    packedData = pickle.dumps(getCommand)
    totalLen = len(packedData)

    s.sendall(struct.pack("i", totalLen))
    s.sendall(packedData)

    replyLen = struct.unpack("i", s.recv(4))[0]
    data = bytearray()
    while (replyLen > len(data)):
        data += s.recv(replyLen - len(data))
    replyCommand = pickle.loads(data)

    print("SongList is: ", replyCommand.payload)
    return replyCommand.payload

# Class for GUI
class Application():
    def __init__(self):
        global s
        self.root = Tk()
        self.root.title("Liqi.Chen 1508274")
        self.frm = Frame(self.root)
        
        #Left
        self.frm_L = Frame(self.frm)

        Label(self.frm_L, text = ' ').pack()
        Label(self.frm_L, text = 'Local Song',
             font =('Arial',10)).pack()

        self.localsong_var = StringVar()
        self.localsong = Listbox(self.frm_L, width=20, height=10,
            listvariable = self.localsong_var)
        for a,b,files in os.walk("Song/"):
            for item in files:
                self.localsong.insert(END, item)
        self.localsong.pack()

        Button(self.frm_L, text="Play",
               command=self.localplay, width=15).pack()
        Label(self.frm_L, text = 'Avaliable PlayLists',
             font =('Arial',10)).pack()

        self.playLists_var = StringVar()
        self.playLists = Listbox(self.frm_L, width=20,
            height=10, listvariable = self.playLists_var)
        self.theplayList = getPlayLists(s) ##### Function 3 Called #####
        # Get all avaliable playlists at start
        for item in self.theplayList:
            self.thelist = str(item) + ". " + self.theplayList[item]
            self.playLists.insert(END, self.thelist)

        Button(self.frm_L, text="Create PlayList",
               command=self.createlist, width=15).pack(side=BOTTOM)

        self.frm_LB = Frame(self.frm_L)
        Label(self.frm_LB, text = 'ListName:', font =('Arial',10),height=1).pack(side=LEFT)
        self.newlistname = StringVar()
        Entry(self.frm_LB, textvariable=self.newlistname,
              width = 10, font =('Arial',10)).pack(side=RIGHT)
        self.frm_LB.pack(side=BOTTOM)
        
        self.playLists.pack()
        self.frm_L.pack(side=LEFT)

        #Mid
        self.frm_M = Frame(self.frm)
        Button(self.frm_M, text="Add Song >>",
               command=self.addsong, width=15).pack(side=TOP)
        Button(self.frm_M, text="<< Get Song",
               command=self.getsong, width=15).pack(side=TOP)
        Label(self.frm_M, text = '\n\n\n\n\n\n\n\n\n\n').pack(side=TOP)
        Button(self.frm_M, text="Get PlayList >>",
               command=self.getplaylist, width=15).pack(side=TOP)
        self.frm_M.pack(side=LEFT)

        #Right
        self.frm_R = Frame(self.frm)
        
        Button(self.frm_R, text="Remove ↓ From Sever",
               command=self.removesong, width=18).pack(side=TOP)
        Label(self.frm_R, text = 'Sever Song',
             font =('Arial',10)).pack()
        
        self.hostsong_var = StringVar()
        self.hostsong = Listbox(self.frm_R, width=20,
            height=10, listvariable = self.hostsong_var)
        self.hostsongList = getSongList(s) ##### Function Called #####
        # Get all avaliable songs at start
        for item in self.hostsongList:
            self.thelist = str(item) + ". " + self.hostsongList[item] + ".mp3"
            self.hostsong.insert(END, self.thelist)
        self.hostsong.pack()

        Button(self.frm_R, text="↓ Add to playlist",
               command=self.addsongtolist, width=15, height=1).pack()

        self.listname = Label(self.frm_R, font =('Arial',10))
        self.listname["text"] = "Songs in PlayList"
        self.listname.pack()
        self.frm_R.pack()

        self.songList_var = StringVar()
        self.songList = Listbox(self.frm_R, width=20,
            height=10, listvariable = self.songList_var)

        self.frm_RB = Frame(self.frm_R)
        Button(self.frm_RB, text="Play",
               command=self.listplay, width=15).pack()
        Button(self.frm_RB, text="Remove Song",
               command=self.removelistsong, width=15).pack()
        self.frm_RB.pack(side=BOTTOM)
        
        self.songList.pack()
        self.frm_R.pack(side=RIGHT)

        self.frm.pack()

    def addsong(self):
        songName = self.localsong.get(self.localsong.curselection())
        songName = songName.replace(".mp3","")
        songID = addSong(songName, s) ##### Function 1 Called #####
        self.hostsong.insert(END, songID + ". " + songName + ".mp3")

    def getsong(self):
        Song = self.hostsong.get(self.hostsong.curselection())
        songID = int(Song.split(". ")[0])
        songName = Song.split(". ")[1].replace(".mp3","")
        count = 0
        localsong = self.localsong_var.get().split(", ")
        for item in localsong:
            if songName in localsong[count]:
                print("The song is exist in local song")
                return
            count = count + 1
        getSongByID(songID, songName, s) ##### Function 5 Called #####
        self.localsong.insert(END, songName + ".mp3")

    def removesong(self):
        Song = self.hostsong.get(self.hostsong.curselection())
        songID = int(Song.split(". ")[0])
        count = 0
        hostsong = self.hostsong_var.get().split(", ")
        for item in hostsong:
            if str(songID)+". " in hostsong[count]:
                self.hostsong.delete(count)
            count = count + 1
        count = 0
        songlist = self.songList_var.get().split(", ")
        for item in songlist:
            if str(songID)+". " in songlist[count]:
                self.songList.delete(count)
            count = count + 1
        removeSong(songID, s) ##### Function 9 Called ######

    def getplaylist(self):
        self.songList_var.set((''))
        playList = self.playLists.get(self.playLists.curselection())
        listID = int(playList.split(". ")[0])
        getPlayList(listID, s) ##### Function 4 Called ######
        f = open("Lists/" + str(listID) + ".txt", "r")
        flag = 0
        for line in f:
            if flag == 0:
                self.listname["text"] = str(listID) + ". " + line.replace("\n","")
                self.listname.pack()
                self.frm_R.pack()
                flag = 1
            else:
                read = line.split(",")
                self.songList.insert(END, read[0] + ". "
                    + read[1].replace("\n","") + ".mp3")
        f.close()

    def createlist(self):
        listName = self.newlistname.get()
        listID = createList(listName, s) ##### Function 2 Called #####
        self.playLists.insert(END, listID + ". " + listName)

    def addsongtolist(self):
        try: # Avoid choosing a wrong item before pressing button
            Song = self.hostsong.get(self.hostsong.curselection())
            songID = int(Song.split(". ")[0])
            songName = Song.split(". ")[1]      
            if self.listname["text"] == 'Songs in PlayList':
                print("Please choose(get) one playlist at first")
            else:
                count = 0
                songlist = self.songList_var.get().split(", ")
                for item in songlist:
                    if str(songID)+". " in songlist[count]:
                        print("Song already exist in the list")
                        return
                    count = count + 1
                listID = int(self.listname["text"].split(". ")[0])
                self.songList.insert(END, str(songID) + ". " + songName)
                EditSong(songID, listID, "add", s) ##### Function 6 Called #####
        except Exception as e:
            print(e)
            return  

    def removelistsong(self):
        Song = self.songList.get(self.songList.curselection())
        songID = int(Song.split(". ")[0])
        count = 0
        songlist = self.songList_var.get().split(", ")
        for item in songlist:
            if str(songID)+". " in songlist[count]:
                self.songList.delete(count)
            count = count + 1
        listID = int(self.listname["text"].split(". ")[0])
        EditSong(songID, listID, "remove", s) ##### Function 6 Called #####

    def localplay(self):
        songName = self.localsong.get(self.localsong.curselection())
        #playsound.playsound("Song/" + songName)
        print("Playing......")

    def listplay(self):
        Song = self.songList.get(self.songList.curselection())
        songID = int(Song.split(". ")[0])
        songName = Song.split(". ")[1].replace(".mp3","")
        count = 0
        flag = True
        localsong = self.localsong_var.get().split(", ")
        for item in localsong:
            if songName in localsong[count]:
                print("The song is exist in local file")
                print("Now using local song file to play")
                flag = False
                break
            count = count + 1
        if flag:
            print(songName)
            getSongByID(songID, songName, s) ##### Function 5 Called #####
            print("Now start playing")
            self.localsong.insert(END, songName + ".mp3")
        #playsound.playsound("Song/" + songName + ".mp3")
        
# main()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
    
root = Application()
mainloop()

s.close()




        

