# battleship

this is a command line adaption of the popular battleship board game.

if you 'Download ZIP' and decompress it, then; </br>
pc- open command prompt and run:  path\battleship_server.py</br>
pc- open a new prompt window and run:  path\battleship_client.py ServerIpAddress Port</br>
osx- open terminal and run:  python path/battleship_server.py</br>
osx- open a new terminal window and run:  python path/battleship_client.py ServerIpAddress Port

'battleship_server.py' will display the ServerIpAddress and Port at runtime.

you can run as many instances of 'battleship_client.py' as you like.</br>
as clients connect to 'battleship_server.py' it will behave as a lobby and 2 x 2 serve them a new game and control it.

when a game ends by annihilation of a players force or the opponent disconnects from the server.</br>
the client will delay 5 seconds before rejoining the servers games queue.

sockets allow the programs to communicate on your local computer or accross your LAN.</br>
it is quite interesting to load the task manager, hone in on python network traffic and watch the data transfer.

those new to python will need to download and install at least python 2.7 available at <a href="https://python.org/downloads">https://python.org/downloads</a>
