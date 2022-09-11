# Artificial Intelligence based Ecosystem Simulator

<div align="center">
  <img src="https://github.com/Shivamroy412/Ecosystem_Simulator/blob/master/img/screenshot.png"><br>
</div>

## Introduction

This project contains a visual Ecosystem Simulator contaning elements from three levels of a food chain. 
The program aims to simulate the basic life processes (movement, eating, reproduction, death) of the creatures
in as natural way as possible without complicating the program too much. The main focus of the program is to 
implement **Neural Networks** using a state of the art **genetic algorithm**.
<br>

## Overview
The simulation contains grass as the bottom most element of the food chain, which keeps spawning at random locations. 
There are two more levels of the food chain which is constituted by rabbits and foxes. At the beginning of the simulation, 
an initial quantity of all the elements spawn at random locations, the animals in which are then moving randomly within 
the map area. Every animal is an instance of either the `Fox` or `Rabbit` class, which inherit from the parent class 
`Organism`. There are several attributes which are speciied within the classes, where most of the attributes have a specific 
range from which during the creation of an instance a random value is assigned to maintain diversity.

Within the assigned life span of the animals, they need to eat to survive. The rabbits need to find grass to survive and
the foxes need to eat rabbit to survive. The animals have a hunger limit in days, before which they would require to eat 
again to survive. The gender of the animals are assigned randomly during their birth and the animals try to find a mate 
of the opposite gender to reproduce. After completion of the gestation period, new off-springs are born which inherit 
attributes from both the parents having equal probabilities of inheriting from either of the parent and a 10% (can be 
changed in the code) chance of mutation.  