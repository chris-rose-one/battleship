# battleship

this is a command line based adaption of the popular battleship board game.

if you download and decompress battleship.zip on your Desktop

pc - open cmd prompt and run:  Desktop\battleship\battleship_server.py</br>
pc - open a new prompt window and run:  Desktop\battleship\battleship_client.py ServerIpAddress 9009
linux - open terminal and run:  python Desktop/battleship/battleship_server.py
linux - open a new terminal window and run:  python Desktop/battleship/battleship_client.py ServerIpAddress 9009

you can run as many instances of 'battleship_client.py' as you like.

as clients connect to 'battleship_server.py' it will 2 x 2 serve them a new game and control its logic.
when a game ends by annihilation of a players force or the opponent disconnects from the server.
the client will delay 10 seconds before rejoining the servers games queue.

sockets allow the programs to communicate on your local computer or accross your LAN
it is quite interesting to load the task manager, hone in on python network traffic and watch the data transfer
