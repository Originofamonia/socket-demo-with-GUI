import socket
import threading
import struct
import pickle
import string
import os

class Command:
    command = ""
    payload = ""

def loadSongDict():
    f = open("Song/songList.txt", "r")
    songDict = {}
    for line in f:
        read = line.split(",")
        songDict[int(read[0])] = read[1].replace("\n","")
    f.close()
    return songDict

def saveSongDict(songDict):
    f = open("Song/songList.txt", "w")
    songlist = []
    for key in songDict:
        songlist.append(str(key))
        songlist.append(",")
        songlist.append(songDict[key])
        songlist.append("\n")
    f.writelines(songlist)
    f.close()

def loadListDict():
    f = open("Lists/playLists.txt", "r")
    listDict = {}
    for line in f:
        read = line.split(",")
        listDict[int(read[0])] = read[1].replace("\n","")
    f.close()
    return listDict

def saveListDict(listDict):
    f = open("Lists/playLists.txt", "w")
    playlist = []
    for key in listDict:
        playlist.append(str(key))
        playlist.append(",")
        playlist.append(listDict[key])
        playlist.append("\n")
    f.writelines(playlist)
    f.close()

def RemoveSongFromList(songID, listID):
    playlist = open("Lists/" + listID + "_playlist.txt", 'r')
    listData = {}
    count = 0
    for line in playlist:
        if count == 0: # The first line is the name of this playlist
            read = line.replace("\n","")
            listData[read] = ""
        else:
            read = line.split(",")
            listData[int(read[0])] = read[1].replace("\n","")
        count = count + 1
    playlist.close()

    if int(songID) in listData:
        listData.pop(int(songID)) # Remove the song
        playlist = open("Lists/" + listID + "_playlist.txt", "w")
        listWrite = []
        count = 0
        for key in listData:
            if count == 0:
                listWrite.append(key)
                listWrite.append("\n")
            else:
                listWrite.append(str(key))
                listWrite.append(",")
                listWrite.append(listDict[key])
                listWrite.append("\n")
            count = count + 1
        playlist.writelines(listWrite)
        playlist.close()
        return True
    else:
        return False

# Class of Thread
class SocketThread(threading.Thread):
    
    def __init__(self, socketInstance):
        threading.Thread.__init__(self)
        self.mySocket = socketInstance
        global songDict
        global listDict
    
    def run(self):
        global songDict
        global listDict
        try:
            while (True):
                print("Reading initial length")
                a = self.mySocket.recv(4)
                print("Wanted 4 bytes got " + str(len(a)) + " bytes")

                if len(a) < 4:
                    raise Exception("Client closed socket, ending client thread")

                messageLength = struct.unpack('i', a)[0]
                print("Message Length: ", messageLength)
                data = bytearray()
                while messageLength > len(data):
                    data += self.mySocket.recv(messageLength - len(data))

                newCommand = pickle.loads(data)
                print("\nCommand is: ", newCommand.command.replace('_',' '))

             
                ClientCommand = newCommand.command.split(" ")
                # Divide the command to recognize it, " " is the divider

                # 1.Adding Songs:
                if ClientCommand[0] == "AddSong":
                    songName = ClientCommand[1].replace('_',' ')
                    #Get the Song Name, The space in song name is replaced by '_' in data transform
                    print("Adding song")

                    songID = 1;
                    for key in songDict:
                        songID = key + 1
                    # Result: ID of new song = ID of the final song + 1

                    music = open("Song/" + str(songID) + ".mp3", 'wb')
                    print("Adding", str(songID) + ".mp3",
                          "(Song Name: " + songName + ")")
                    music.write(newCommand.payload)
                    music.close() # Save the song as .mp3 file

                    songDict[songID] = songName
                    saveSongDict(songDict) # Add the song to songlist

                    replyCommand = Command()
                    replyCommand.command = "SongAdded " + str(songID)

                # 2.Creating a playlist:
                elif ClientCommand[0] == "CreatePlayList":
                    listName = ClientCommand[1].replace('_',' ') #Get the playlist Name
                    print("Creating playlist")

                    listID = 1;
                    for key in listDict:
                        listID = key + 1 # Result: ID of new list = ID of the final list + 1

                    playlist = open("Lists/" + str(listID) + "_playlist.txt", 'w')
                    print("Creating", str(listID) + "_playlist.txt",
                          "(List Name: " + listName + ")")
                    playlist.write(listName + "\n")
                    playlist.close() # Save the playlist

                    listDict[listID] = listName
                    saveListDict(listDict) # Add the song to songlist

                    replyCommand = Command()
                    replyCommand.command = "PlayListCreated " + str(listID)

                # 3.Download a list of playlists available:
                elif ClientCommand[0] == "GetAllPlayLists":
                    print("Sending playlists")
                    replyCommand = Command()
                    replyCommand.command = "AllPlayList"
                    #f = open("Song/songList.txt", "r")
                    #playlists = f.read().replace("\n",",")
                    #playlists = playlists.split(",")
                    #playlists.pop() # At the end of file there is a \n
                    #f.close()
                    #replyCommand.payload = playlists # Return type is python list
                    replyCommand.payload = listDict

                # 4.Download a playlist: (by playlistID)
                elif ClientCommand[0] == "GetPlayList":
                    playlistID = ClientCommand[1]       #Get the Song ID
                    print("Sending playlist")
                    replyCommand = Command()
                    
                    if int(playlistID) not in listDict:  # Check if the Song ID exist
                        raise Exception("File not found")
                    
                    playlist = open("Lists/" + playlistID + "_playlist.txt", 'rb')
                    print("Sending", playlistID + "_playlist.txt",
                          "(List Name: " + listDict[int(playlistID)] + ")")
                    replyCommand.payload = playlist.read()
                    replyCommand.command = "PlayListList"
                    playlist.close()

                # 5.Download a song by songID:
                elif ClientCommand[0] == "GetSong":
                    SongID = ClientCommand[1]       #Get the Song ID
                    print("Sending song")
                    replyCommand = Command()
                    
                    if int(SongID) not in songDict:  # Check if the Song ID exist
                        raise Exception("File not found")
                    
                    music = open("Song/" + SongID + ".mp3", 'rb')
                    print("Sending", SongID + ".mp3","(" + songDict[int(SongID)] + ")")
                    replyCommand.payload = music.read()
                    music.close()
                    replyCommand.command = "SongData"

                # 6.1.Add song to a playlist:
                elif ClientCommand[0] == "AddSongToList":
                    songID = ClientCommand[1]
                    listID = ClientCommand[2]
                    print("Adding song to playlist")

                    songName = songDict[int(songID)] # get the song name
                    songData = songID + "," + songName + "\n"

                    playlist = open("Lists/" + listID + "_playlist.txt", 'r')
                    listData = {}
                    count = 0
                    for line in playlist:
                        if count == 0: # The first line is the name of this playlist
                            read = line.replace("\n","")
                            listData[read] = ""
                        else:
                            read = line.split(",")
                            listData[int(read[0])] = read[1].replace("\n","")
                        count = count + 1
                    playlist.close() # To get the songlist data

                    playlist = open("Lists/" + listID + "_playlist.txt", 'a')
                    print("Adding song(ID: " + songID + ") to " + listID + "_playlist.txt")

                    replyCommand = Command()
                    if int(songID) not in listData: # Whether song is already in the songlist
                        playlist.write(songData)
                        replyCommand.command = "SongAdded"
                    else:
                        replyCommand.command = "SongAddedBefore" # if song exist in this songlist
                    playlist.close()

                # 6.2.Remove song from a playlist:
                elif ClientCommand[0] == "RemoveSongFromList":
                    songID = ClientCommand[1]
                    listID = ClientCommand[2]
                    print("Removing song to playlist")
                    print("Removing song(ID: " + songID + ") from " + listID + "_playlist.txt")

                    replyCommand = Command()

                    if RemoveSongFromList(songID, listID):
                        replyCommand.command = "SongRemoved"
                    else:
                        replyCommand.command = "SongNotInList"

                # 9.Remove a song from the server:
                elif ClientCommand[0] == "RemoveSong":
                    songID = ClientCommand[1]
                    print("Removing song")

                    try: # Remove the song file
                        os.remove("Song/" + songID + ".mp3")
                    except Exception as e:
                        print(e)
                        
                    # Remove the song from songlist
                    songDict.pop(int(songID))
                    saveSongDict(songDict)

                    count = 1
                    while True: # Remove the song from all playlist
                        if os.path.exists("Lists/" + str(count) + "_playlist.txt"):
                            remove = RemoveSongFromList(int(songID), str(count))
                            count = count + 1
                        else:
                            break
                    replyCommand = Command()
                    replyCommand.command = "SongRemovedOK"

                # Get all the avaliable songs
                elif ClientCommand[0] == "GetSongList":
                    print("Sending song list")
                    replyCommand = Command()
                    replyCommand.command = "SongList"
                    replyCommand.payload = songDict
                    
                else:
                    print("Unknown Command:", newCommand.command.replace('_',' '))
                    raise Exception("Unknown Command")

                packedData = pickle.dumps((replyCommand))               # Serialize the class to a binary array
                self.mySocket.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
                self.mySocket.sendall(packedData)

        except Exception as e:
            print(e)
            print("\nClosing socket")
            self.mySocket.close()

#start our main....

host = "localhost"
port = 4567

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(1)

print("Listening...")

songDict = loadSongDict() # Server load all the ID and names of songs at start
print(songDict.items())
listDict = loadListDict() # Server load all the ID and names of songlists at start
print(listDict.items())


while True:
    (clientSocket, address) = serverSocket.accept()
    print("Got incoming connection")
    newThread = SocketThread(clientSocket)        # make a new instance of our thread class to handle requests
    newThread.start()                             # start the thread running....
    

    
