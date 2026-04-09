# NEAT-Powered AI Agents through the game of Pong
Training &amp; Dueling Programs for NEAT-Python optimized AI Agents in Environments of Scaling Difficulty.

**Instructions:**

```pong_power.py``` is the base pong game version without AI agents & NEAT Algorithms.

```pong_final_power_up.py``` is the NEAT-AI training program that takes parameters from ```config-final_power_up.txt```.

```duel_ai``` is a Vibe Coded Program with Google's Gemini, which allows importing of AI-agents through ```.pkl``` files to be dueled up against each other. Both NEAT-networks run the current network topology, but don't mutate. This program also imports classes from ```pong_final_power_up.py``` so make sure they are in the same folder.

**TO DUEL AI**:

1. install dependencies through ```requirements.txt```.

2. Pass two ```.pkl``` files as function parameters on Line 87 of the ```duel_ai``` program.
   
3. Make sure ```pong_final_power_up.py``` and ```config-final_power_up.txt``` are in the same folder as this program, as classes and parameters are taken from these programs.
   
4. Run the ```duel_ai``` program.

**TO TRAIN AI**

1. Set Fitness, Topology, & Evolutionary Parameteres on ```config-final_power_up.txt```.
   
2. Configure ```pong_final_power_up.py``` accordingly, then run the program. You may press the "F" key to pass 1000 frames into the program, speeding up the process. Then you can press "S" to return to 60 FPS.

DISCLAIMER: Some Code is Vibe Coded and aligns with Educational Requirements for the Machine Learning Course at University Canada West. This project was done for Educational Purposes only. 

Useful Links:

NEAT-Python Documenation - https://neat-python.readthedocs.io/en/latest/
Tech with Tim NEAT Pong Video - https://www.youtube.com/watch?v=2f6TmKm7yx0&t=57s
NEAT Algorithm Visually explained by David Schäfer - https://www.youtube.com/watch?v=yVtdp1kF0I4&t=26s
