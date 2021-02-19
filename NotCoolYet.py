## OOP

class cookie():
    def __init__(self, r,flavor):
        self.radius = r
        self.theFlavor = flavor

    def area(self):
        return 3.1416 * self.radius * self.radius
    
    def perimeter(self):
        return 2 * 3.1416 * self.radius

smallCookie = cookie(3,'rasin')
largeCookie = cookie(10,'chocolate')

# smallCookie
print("My small cookie is a " + smallCookie.theFlavor + " cookie.")
print("It's area is: ")
print(smallCookie.area())
print("And it's perimeter is: ")
print(smallCookie.perimeter())

# largeCookie
print("My large cookie is a " + largeCookie.theFlavor + " cookie.")
print("It's area is: ")
print(largeCookie.area())
print("And it's perimeter is: ")
print(largeCookie.perimeter())