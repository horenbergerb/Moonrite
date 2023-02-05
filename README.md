# Moonrite

Moonrite is a collection of computer vision tools for Old School Runescape.

Moonrite can do many things, such as estimate play location from the minimap, route-find on the world map, and detect interactible objects in the game.

Additionally, Moonrite is designed to do these things quickly, so that you can get results for real time applications.

# Requirements

To use Moonrite, you will need

- A Linux machine with X11 support (Runescape needs a screen)
- Docker

# Setup

To set up Moonrite, run

```
./build.sh
```

# Running Moonrite

To run Moonrite, run

```
./run.sh
```

Then, you may begin the main program by running

```
python3 moonrite.py
```