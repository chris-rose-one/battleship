# battleship

this is a command line adaption of the popular battleship board game.

sockets allow these programs to communicate on your local computer or accross your LAN.

those new to python will need to download and install python 2.7 available at <a href="https://python.org/downloads">https://python.org/downloads</a>

if you 'Download ZIP' and decompress it, then; </br>
pc- open command prompt and run:  path\battleship_server.py</br>
pc- open a new prompt window and run:  path\battleship_client.py ServerIpAddress Port</br>
osx- open terminal and run:  python path/battleship_server.py</br>
osx- open a new terminal window and run:  python path/battleship_client.py ServerIpAddress Port

'battleship_server.py' will display the ServerIpAddress and Port at runtime.

you can run as many instances of 'battleship_client.py' as you like.</br>
as clients connect to 'battleship_server.py' it will behave as a lobby and 2 x 2 serve them a new game and control it.

when a game ends by annihilation of a players force or the opponent disconnects from the server.</br>
the client will delay 10 seconds before rejoining the servers games queue.

in the '__main__' method at the bottom of 'battleship_server.py' are 3 variables which set the games parameters;

board_space
- 10 will deliver a 10x10 square board but, change it to 5 and play on a 5x5 square board
- a number > 10 will break the views print out of the board

available_ships
- a list of tuples which each declare a ships name and how many spaces long it is
- with in reason you could; make ships longer or shorter, add ships, remove ships...

salvo mode
- when set to False, you get the typical back and forth, i attack you, you attack me style of game play
- but, when set to True, a player on their turn will make a No. of attacks equal to thier No. of ships still floating
