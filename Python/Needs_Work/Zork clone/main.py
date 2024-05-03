from pack import NameGenerator as name_gen
from pack import Zone
import os

os.system('cls')

firstZone = Zone.zone(0, 0, [], "Test Zone")
firstZone.print_zone()
print()
firstZone.print_desc()