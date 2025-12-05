class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point Info: {self.x, self.y, self.z}"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z