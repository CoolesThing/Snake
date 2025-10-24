Snake

Description:
The project Snake is a demonstration of a simple bot operating within the game snake inspried by the "Google Snake Game". The game is built in python using the pygame package. 
    To play the game manually, simply follow the on-screen instructions. 
    To let the bot play the game for you, press 'b' to toggle the bot on or off durring gameplay.
Observe your score in the terminal.

Installation:
Ensure you have Python 3.11.9 installed
Install dependencies (pip install -r requirements.txt)

How to run:
In your python powershell termnial enter the following commands to start the game...

cd ...\code
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python snake.py

Controls:
The game uses the inputs WASD to move the snake around the screen.
To allow the bot to play the game, press 'b' to toggle the bot.
To end the game or close the program, press 'esc'.

Known issues:
Pressing 'esc' while the bot is on does not stop the program, must toggle bot off first.
The snake is allow to make an illegal move on the first key press of the game.
On death, no debounced keys allows for easy miss-inputs to start the next game without intent.
All rounds end in game over, no win screen for 100% wins.
No active score board, score is printed in the terminal window.

Credits:
Tyler Giczkowski
Aidan VandenElzen
M365 Copilot