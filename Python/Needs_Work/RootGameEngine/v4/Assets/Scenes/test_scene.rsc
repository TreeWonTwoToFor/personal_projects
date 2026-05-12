camera 10 0 0 0 -90 0
light 10 5 5 75
background 0 0 25

open red cylinder/cylinder.obj cylinder/red_texture.bmp
open checkered cylinder/cylinder.obj cylinder/checkered_texture.bmp
open blue cylinder/cylinder.obj cylinder/blue_texture.bmp

translate red 0 0 -2.5
translate blue 0 0 2.5

open box cube/cube.obj
translate box 0 5 0
scale box 0.4 0.4 0.4

# rotate testing
rotate red 1 0 0 10
rotate checkered 0 1 0 10
rotate blue 0 0 1 10

orbit box 1 0 0 90