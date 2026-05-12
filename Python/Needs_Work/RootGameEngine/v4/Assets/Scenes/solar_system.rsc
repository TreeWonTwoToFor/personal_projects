camera 0 25 25 45 -180 0

open sun icosphere/icosphere.obj
open mercury icosphere/icosphere.obj
open venus icosphere/icosphere.obj
open earth icosphere/icosphere.obj
open mars icosphere/icosphere.obj
open jupiter icosphere/icosphere.obj
open saturn icosphere/icosphere.obj
open uranus icosphere/icosphere.obj
open neptune icosphere/icosphere.obj

translate sun 0 0 0
scale sun 10 10 10

translate mercury 0 0 4
scale mercury 0.5 0.5 0.5

translate venus 0 0 6
scale venus 0.7 0.7 0.7

translate earth 0 0 8
scale earth 1 1 1

translate mars 0 0 10
scale mars 1 1 1

translate jupiter 0 0 12
scale jupiter 1 1 1

translate saturn 0 0 14
scale saturn 1 1 1

translate uranus 0 0 16
scale uranus 1 1 1

translate neptune 0 0 18
scale neptune 1 1 1

# planetary rotation
/ 88 days
orbit mercury 0 1 0 149.3
/ 225
orbit venus   0 1 0 58.4
/ 365
orbit earth   0 1 0 36
/ 687
orbit mars    0 1 0 19.13
/ 4,333
orbit jupiter 0 1 0 3.03
/ 10,759
orbit saturn  0 1 0 1.22
/ 30,687
orbit uranus  0 1 0 0.428
/ 60,190
orbit neptune 0 1 0 0.218
