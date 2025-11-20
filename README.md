Snake

Description:
The project Snake is a demonstration of an implementtion of a NEAT algorithm that neural networks capable of playing the game snake. There are two ways to run this code. The first is to play the game snake independent of any NN. The second is the run a NEAT algorithm to attempt to create functional bots to play the game. The intruction to do either is below.

Installation:
Ensure you have Python 3.11.9 installed
Install dependencies (pip install -r requirements.txt)

How to run the independent game:
In your python powershell termnial enter the following commands to start the game...

cd ...\code
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m snake.py

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

How to run the neat algorithm (assuming a venv is already created and activated and has installed requirements):

cd ...\code
python main.py

Info:
The main.py file uses the config.txt file to configure the NEAT algorithm. There the pop size and other relevant NEAT configurations are set.

The main.py runs as follows. The program is set to run for X generations (set to 100). After 100 generations has passed, the best genmone "winner" of the last generation is set to play the game to showcase the results.

While the program runs, a blank pygame window will open (blank to speed up train time). Additionaly, the terminal will print the following to keep you, the user updated:

    ****** Running generation ## ******

    Population's average fitness: ##.## stdev: ##.##
    Best fitness: ##.## - size: (#, #) - species # - id ####
    Average adjusted fitness: #.##
    Mean genetic distance #.###, standard deviation #.###
    Population of 150 members in 4 species (after reproduction):
    ID   age  size   fitness   adj fit  stag
    ====  ===  ====  =========  =======  ====
        3   11    40   1185.659    0.112     9
        4   11    27    161.300    0.052     8
        5   10    45   1268.992    0.105     3
        6    3    38   1118.992    0.104     0
    Total extinctions: 0
    Generation time: 0.160 sec (0.149 average)

How to interact with main.c:

There are many places where you the user can adjust certian aspects of the code to produce a better NN. The following is a helper:

    line  121: Here you can change the maximum steps the snake can take without eating an apple

    lines 172 - 175: here, uncommenting will allow you to see the training in real time, but at a cost of compute time, as rendering is computationally intense.

    lines 188 - 210: Here is the fitnness function claculation. Changing the code here will change how the algorithm determines a solutions' value.

    line 223: here is a commented out line of code, which if un commeneted, will allow you to start your training from a saved state.

    line 230: here you can change the number of generations the program will run for.

    line 251: commenting out this line will allow the 'winner' to play. To do so, you must have at a best_genome.pkl file which is produced at the end of a main.py run.

Credits:
Tyler Giczkowski
Aidan VandenElzen
M365 Copilot