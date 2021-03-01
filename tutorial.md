# pypew: A tutorial for [Pyxel](https://github.com/kitao/pyxel)

This tutorial aims to provide a quick and dirty getting started guide for pyxel.
The game has obvious flaws and the tutorial will not cover all features of the engine.

## What is Pyxel?

Pyxel is a retro game engine with restrictions on colors, sound channels and draw area 
([Specs](https://github.com/kitao/pyxel#Specifications)).
This leads to a simpler engine, and games can take advantage of the special circumstances.
For example, the final game will detect collision by pixel color.

Pyxel only provides operations to draw, play sounds and detect input, so you will have to
either provide your collision detection and physics yourself or use one of the many libraries.

## Installation

On Linux, it should suffice to install pyxel via pip or in your favorite IDE.
I recommend following the instructions at [GitHub](https://github.com/kitao/pyxel#how-to-install).

This will also include some further samples for Pyxel.

## How to use this tutorial

This file contains the lessons, and the numbered folders contain the final files
from every lesson. The goal is a small space shooter, with some sounds and simple hit detection.

## 01 Game Setup

The most basic game you can create in Pyxel displays nothing but a black screen.
To do this, we need to do 3 things:

1. import pyxel
2. initialize pyxel
3. run pyxel
