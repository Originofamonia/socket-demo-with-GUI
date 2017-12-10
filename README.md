# Python-socket-example-with-GUI
### Before pressing the button in GUI, item in Listbox MUST BE correctly selected.
<br>
Both Sever and Client contain two file folders called ‘Song’ and ‘Lists’. The folder ‘Song’ is used to hold song file, and in Server there is one more list(songList.txt) which record all the name and id of available song. The folder ‘Lists’ is used to hold the playlist, and in Sever there is also a list(playLists.txt) which contains all the name and id of available playlists. At beginning, the folder ‘Lists’ of Client is empty, and these .mp3 file in folder ‘Song’ of Client means client’s local song. Client can download or upload playlist or song from Server and save it in the folder.
<br>
Data format in playlists: <br>
<playlist name> <br>
<SongID>, <SongName>…… <br>
For example, in 1_playlist.txt:<br>
List A <br>
1,Song A <br>
3,Song C <br>
When Sever reading these files, it will return a Python Dict. <br>
