camera 0 0 10 0 180 0
background 100 100 255

 / bird setup
open bird icosphere/icosphere.obj
scale bird 0.5 0.5 0.5

open pipe_1 cylinder/cylinder.obj
open pipe_2 cylinder/cylinder.obj
open pipe_3 cylinder/cylinder.obj
open pipe_4 cylinder/cylinder.obj
open pipe_5 cylinder/cylinder.obj
open pipe_6 cylinder/cylinder.obj

scale pipe_1 1 100 1
scale pipe_2 1 100 1
scale pipe_3 1 100 1
scale pipe_4 1 100 1
scale pipe_5 1 100 1
scale pipe_6 1 100 1

translate pipe_1 -8 -5.5 0
translate pipe_2 -8 5.5 0
translate pipe_3 -16 -6.5 0
translate pipe_4 -16 4.5 0
translate pipe_5 -24 -4.5 0
translate pipe_6 -24 6.5 0

# move pipes
translate pipe_1 2 0 0
translate pipe_2 2 0 0
translate pipe_3 2 0 0
translate pipe_4 2 0 0
translate pipe_5 2 0 0
translate pipe_6 2 0 0

/ make the bird fall
translate bird 0 -2 0
