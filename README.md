# FeiXingQi

## Table of Contents

- [Project Info](#project-info)
- [Summary](#summary)
- [Requirements](#requirements)
- [Installation](#installation)

## Project Info
CMPT 276 Project by Team Fawn

Members:
- Eric - ysw6@sfu.ca
- Zhengying - zsa65@sfu.ca
- Chris - casoo@sfu.ca
- Curtis Grotzke - cjg17@sfu.ca
- Grayson - graysonl@sfu.ca

## Summary
In [FeiXingQi (飞行棋）](https://www.ymimports.com/pages/how-to-play-aeroplane-chess-fei-xing-qi) or Aeroplane Chess, there are 2-4 players in a game, who play with the goal of getting all their planes from their respective bases into the centre of the game board. 

Official General Rules For The Base Game:
* A six-sided die is used to determine the movement of a player's respective plane(s)
* The player is able to launch a plane from their base once a 6 is rolled
* If a player rolls six, they are able to roll again
* The board will indicate the direction
* Each player has a corresponding colour. While traversing the board, if one of their planes lands on their colour, they are able to jump to the next tile of the same colour.
* Each player has a special tile corresponding with their colour which enables the player to jump a plane across the board.
* The winning condition is met once all of a player's planes has reached the centre base.  

Potential New Gamemode Made (**STILL IN DESIGN**): 
* **A brand new win condition**: based on a scorepoint system, the player with the most points achieved under a timed session wins the game
* Every tile a player moves across is one point gained, with some special tiles gaining multiple points
* A plane reaching centre base will now be rewarded a large sum of points instead
* Planes now also carry missiles, with the capability to shoot enemy planes down for points
* **Sudden events**: Sudden Events will appear when certain tiles are reached. Sudden events could be both beneficial or harmful to a single player or every player on the playing field 
* An all-new **Aliance System**: Players can now form an alience of two with icon indications. Under an allience, points achieved by one player will also be rewarded to the other player. However, alliences can be broken... by shooting their plane down and earning double the point for you

## Wireframes
Wireframes can be found on [figma](https://www.figma.com/file/jqpiSDFuiUwqegEEUoQVvs/Spaceship-Chess-Wireframes?type=design&node-id=0%3A1&mode=design&t=6kDsDAlBPjDvWAsf-1)
## Requirements
**This game requires the Pygame library to play**
If Pygame is not installed it can installed with the following methods (requires Python):

Using Pip:

`
python3 -m pip install -U pygame --user
`

For Windows

`
py -m pip install -U pygame --user
`

For Mac OS X:

`
python3 -m pip install -U pygame --user
`

For Ubuntu:

`
sudo apt-get install python3-pygame
`


## Installation
Via https
```bash
git clone https://github.sfu.ca/graysonl/FeiXingQi.git
cd FeiXingQi
```
or 
Via ssh
```bash
git clone git@github.sfu.ca:graysonl/FeiXingQi.git
cd FeiXingQi
```
