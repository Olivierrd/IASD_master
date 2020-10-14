# Monte Carlo

## Course 

Introduction to Monte Carlo for computer games. Monte Carlo Search has revolutionized computer games. It works well with
Deep Learning so as to create systems that have superhuman performances in games such as Go, Chess, Hex or Shogi. It is
also appropriate to address difficult optimization problems. In this course we will present different Monte Carlo 
search algorithms such as UCT, GRAVE, Nested Monte Carlo and Playout Policy Adaptation. We will also see how to 
combine Monte Carlo Search and Deep Learning. The validation of the course is a project involving a game or an 
optimization problem.

## Project : Python Easy Chess GUI
A Chess GUI based from Python using PySimpleGUI and Python-Chess modules. Users can also load a chess engine and play with it. This program is based on a [demo chess against ai](https://github.com/PySimpleGUI/PySimpleGUI/tree/master/Chess) from PySimpleGUI.<br>

We didn't implemented the game motor, neither the UI only the Monte Carlo IA.

The IA implemented are :
- UCB
- UCT
- RAVE (soon)
- GRAVE (soon)
- PUTC (soon)

The game motor and the UI was taken from : https://github.com/fsmosca/Python-Easy-Chess-GUI
![](https://i.imgur.com/DT0lOO2.png)

Thank you to :
- Olivier RANDAVEL
- Kenza HAMMOUD
- Louis FONTAINE

### A. Requirements
Windows exe file will be available upon release. In the meantime to get it running the following are required.
* Python 3.7 and up
* Python-chess v0.28.0 and up
* PySimpleGUI 4.4.1 and up
* Pyperclip


### C. Installation
1. If you want to run from the source code
* Python Easy Chess GUI<br>
Download the files including the Images, Engines and Book directories. You can use your favorite uci chess engine like stockfish by copying it into the engines dir.
* Python 3<br>
https://www.python.org/downloads/
* Python-Chess<br>
https://github.com/niklasf/python-chess<br>
pip install python-chess
* PySimpleGUI<br>
https://github.com/PySimpleGUI/PySimpleGUI<br>
pip install pysimplegui
* Pyperclip<br>
https://github.com/asweigart/pyperclip<br>
pip install pyperclip
2. If you want to run from the exe
* Download the exe file from the release link

### D. How to
#### To start the gui
* Execute python_easy_chess_gui.py<br>
Typical command line:<br>
`python python_easy_chess_gui.py`
* Execute the exe when using exe file


### E. Credits
* PySimpleGUI<br>
https://github.com/PySimpleGUI/PySimpleGUI
* Python-Chess<br>
https://github.com/niklasf/python-chess
* Pyperclip<br>
https://github.com/asweigart/pyperclip
* The Week in Chess<br>
https://theweekinchess.com/
* PyInstaller<br>
https://github.com/pyinstaller/pyinstaller
* pgn-extract<br>
https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/
* Python-Easy-Chess-GUI<br>
https://github.com/fsmosca/Python-Easy-Chess-GUI

This project was graded 15/20
