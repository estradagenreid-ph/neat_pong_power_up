# NEAT-Powered AI Agents through the Game of Pong

Training and dueling programs for NEAT-Python agents in a Pong environment with power-ups and increasing difficulty. This project was made for the Machine Learning course at University Canada West.

**Instructions:**

Install Python, clone the repository, and create a virtual environment:

```sh
git clone https://github.com/estradagenreid-ph/neat_pong_power_up.git
cd neat_pong_power_up
python -m venv .venv
```

Install dependencies on Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On macOS/Linux:

```sh
./.venv/bin/python -m pip install -r requirements.txt
```

Use that same virtual environment's Python for the commands below. On Windows this is `.\.venv\Scripts\python.exe`; on macOS/Linux it is `./.venv/bin/python`. A desktop display is needed for the Pygame window.

**FILES:**

| File | What it does |
| --- | --- |
| `pong_power.py` | Two-player Pong with power-ups, without NEAT agents. |
| `pong_final_power_up.py` | NEAT training program and shared game classes. |
| `config-final_power_up.txt` | Fitness, population, network topology, and evolutionary parameters. |
| `duel_ai.py` | Loads two saved genomes and runs their networks against each other without evolution. |
| `GEN ... AI.pkl` | Saved example genomes from different training generations. |
| `requirements.txt` | Pygame and NEAT-Python. The other imports are built into Python. |

**TO PLAY WITHOUT AI:**

Run `python pong_power.py`. W/S control the left paddle, and Up/Down control the right paddle. Escape exits.

**TO DUEL AI:**

1. Keep `duel_ai.py`, `pong_final_power_up.py`, `config-final_power_up.txt`, and the saved genomes in the same folder.
2. Run `python duel_ai.py` from that folder. The default match uses `GEN 10 AI.pkl` and `GEN 81 AI.pkl`.
3. To change the agents, edit the two filenames in the `duel_ai(...)` call under `if __name__ == "__main__":` in `duel_ai.py`. Close the window to finish.

Only load pickle files you trust: Python pickle files can execute code when loaded. Saved genomes must also be compatible with the installed NEAT-Python version and network configuration.

**TO TRAIN AI:**

1. Set fitness, population, topology, and evolution parameters in `config-final_power_up.txt`. The game supplies five inputs and expects three outputs, so keep those dimensions unless you also change the game code.
2. Adjust the game settings and reward logic in `pong_final_power_up.py` if needed.
3. Run `python pong_final_power_up.py`. F switches to the fast mode, S returns to 60 FPS, F11 enters fullscreen, and Escape exits. Fast mode targets up to 1,000 FPS; it does not skip a fixed number of frames.
4. Power-ups start when the generation counter reaches 30 and `POWER_UPS` is enabled.
5. When the training run finishes, it saves `best_ai.pkl`. Closing the window early does not save that final file. Optional checkpointing is disabled by default; `SAVE_CHECKPOINTS` enables files with the existing `pong-checkpont-` prefix.

The dependencies are not version-pinned. If the configuration or saved genomes fail with a newer NEAT-Python release, use the version they were created with or migrate the configuration and genomes together.

**TOOLS & ACKNOWLEDGMENTS:**

Pygame handles the game window and rendering. NEAT-Python provides the evolutionary algorithm and neural networks.

Google's Gemini helped with `duel_ai.py` and the power-up drawing code, as acknowledged in the original README and source comments. Codex helped revise the documentation, dependency list, and ignore rules.

Some code was vibe coded. This is an educational project; the saved generations are examples rather than a claim of benchmark performance.

**LOCAL OUTPUTS:**

`.gitignore` excludes environments, secrets, caches, `best_ai.pkl`, and training checkpoints. The existing `GEN ... AI.pkl` examples remain part of the repository.

**Useful links:**

- [NEAT-Python documentation](https://neat-python.readthedocs.io/en/latest/)
- [Pygame documentation](https://www.pygame.org/docs/)
- [Tech With Tim: NEAT Pong](https://www.youtube.com/watch?v=2f6TmKm7yx0&t=57s)
- [David Schäfer: NEAT visually explained](https://www.youtube.com/watch?v=yVtdp1kF0I4&t=26s)
