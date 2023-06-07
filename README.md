# Proiect_PPython
The classic bubble-buster game, implemented in python using pygame library. 
# Window structure

1. Menu
2. bubble wall:
   - A matrix of rectangles of size row\*columns
   - each rectangle contains a bubble
   - rectanglex are drawn for figuring out of collision areas (two adiacent rectangles/squares will pop if the circle/bubble inside have same color)
3. Screen split up in three:
   - upper menu (score and shit)
   - main game screen
   - lower window (ball to be shot, next colors)
