###Runescape Bot Watch

###Problem

With my first version, I spent a lot of time attempting to simulate mouse movements as humans do. It was an extremely difficult task as humans do not take straight lines between targets, and certainly not with the same speed that a computer could reject. I was basically attempting to program my pathing function to take a non-optimal path at a non-optimal speed and do so differently each time. EG, It also cannot follow the same bezier curve as that would be obvious. Plus all those other random interactions humans use with the mouse like idling, wiggling the cursor, highlighting random stuff, all needed to take into consideration to avoid the ban hammer. 

###Solution

This is a new take on Runescape botting with openCV which ran for over a year without detection. The solution was simple, why waste so much time attempting to perfect code to mimic a human-mouse movement, when we already have something that can do it perfectly, my hand.

The thought process would be I download a ghost mouse program that records my mouse movements as I play the game regularly, once the sequence is recorded, I would integrate those movements into my code. 

Now, the mouse movements looked exactly like a human, since every movement done with the mouse was just running a sequence that I recorded. Furthermore, I would record multiple sequences of the same movement to make it even harder to detect.

### Progress


### Done
- log in and shuffle all instances of Runescape on the screen
- Using openCV, it would scan mini map constantly to detect if the bot ever goes out of sequence. (from lag, 6h timeout, rng factors)
- breaks out of botting sequence if the bot sees it has gone out of sync and automatically attempts to fix itself
-If bots could not fix themselves, send me a notification



# RunescapeBotWatch
pip install pywin32
pip install pyautogui
pip install opencv-python
pip install matplotlib
pip install pynput
pip install psutil
.\pip.exe install scipy
