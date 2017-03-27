# WikipediaX2Y
A python script that attempts to play the game of getting from one Wikipedia page to another in as few steps as possible.

## The game
Two or more players race against each other to get from the source Wikipedia page to the destination page by merely clicking on links. 
The winner is either the person who finds the page with the lowest number of clicks or in the shortest amount of time depending on interpretation.

#
This script uses a simple web-crawler to perform a breadth first search of Wikipedia from the source page in the hopes of finding the destination eventually. 

In reality it won't do so in any time of use due to poor design. The script currently works through a group of independent nodes 
travelling through the web and spawning a new node for every page *IT* has not already encountered. This means that although individual
nodes are capable of preventing cycles, the collective processes pages without considering if another node has already done so, causing heavy redundancy.

I plan to amend this issue in the near future by implementing a proper graph structure as opposed to the existing system of individual collections of strings.
