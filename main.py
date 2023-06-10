
import sys
import pygame
from math import acos, asin, pi, sin, cos


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def step_down(self, step: float):
        self.y += step

    def step_left(self, step: float):
        self.x -= step

    def step_right(self, step: float):
        self.x += step

    def step_up(self, step: float):
        self.y -= step

    def step_all(self, step_x: float, step_y: float):
        self.x += step_x
        self.y += step_y

    def get_coordinate(self):
        return self.x, self.y


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.resistance_coefficient = float(3/512)

    def get_canvas(self):
        return self.width, self.height


class Circle:

    boost_x: float = 0
    boost_y: float = 0
    def __init__(self, coordinate: Coordinate, sped_x: float, sped_y: float, color:tuple, radius: float, wall: Canvas):
        self.coordinate = coordinate
        self.sped_x = sped_x
        self.sped_y = sped_y
        self.color = color
        self.radius = radius
        self.wall = wall



    def move(self, dt):
        self.sped_x += self.boost_x - (self.sped_x * self.wall.resistance_coefficient)
        self.sped_y += self.boost_y - (self.sped_y * self.wall.resistance_coefficient)
        #print(f"sped_x: {self.sped_x}\tsped_y: {self.sped_y}")
        self.coordinate.step_all(dt * self.sped_x, dt * self.sped_y)

    def get_coordinate(self):
        return self.coordinate.get_coordinate()

    def hit_wall(self,):
        if (self.coordinate.x - self.radius <= 0) or (self.coordinate.x + self.radius >= self.wall.width):
            self.sped_x = -self.sped_x
        if (self.coordinate.y - self.radius <= 0) or (self.coordinate.y + self.radius >= self.wall.height):
            self.sped_y = -self.sped_y

    def hit_other_circle(self, other):
        flag = False
        for x_point, y_point in self.points:
            flag = flag or (((x_point - other.get_coordinate()[0]) ** 2 +
                             (y_point - other.get_coordinate()[1]) ** 2
                             ) ** 0.5 <= other.radius
                            )
        return flag

    def set_boost_x(self, boost: float = 0):
        self.boost_x = boost

    def set_boost_y(self, boost: float = 0):
        self.boost_y = boost

    def make_acceleration_up(self, boost: float = 3):
        self.boost_y = -boost

    def make_acceleration_down(self, boost: float = 3):
        self.boost_y = boost

    def make_acceleration_left(self, boost: float = 3):
        self.boost_x = -boost

    def make_acceleration_right(self, boost: float = 3):
        self.boost_x = boost

    def upgrade(self, dt, other):
        self.hit_wall()
        self.move(dt)
        self.points = [(cos(angel / 360 * pi * 2) * self.radius + self.get_coordinate()[0],
                        sin(angel / 360 * pi * 2) * self.radius + self.get_coordinate()[1])
                       for angel in range(0, 361, 30)]
        speed = ((self.sped_y)**2 + (self.sped_x)**2)**0.5
        if speed < 512:
            self.color= (int(speed/2), self.color[1], self.color[2])
        else:
            self.color=(255, self.color[1], self.color[2])
        print(self.hit_other_circle(other))




def main():
    print(f"[+] Start project")
    canvas = Canvas(width=500, height=500)
    screen = pygame.display.set_mode(canvas.get_canvas())
    pygame.display.set_caption('YAHOOOO')
    clock = pygame.time.Clock()
    print(f"[+] create canvas")
    coordinate = Coordinate(x=30, y=30)
    coordinate_other = Coordinate(x=250, y=250)
    circle_boss = Circle(coordinate, sped_x=30, sped_y=30, color=(150, 10, 50), radius=20, wall=canvas)
    circle_other = Circle(coordinate_other, sped_x=0, sped_y=0, color=(15, 50, 50), radius=20, wall=canvas)
    while True:
        dt = clock.tick(50) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                    circle_boss.set_boost_y(0)
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                    circle_boss.set_boost_x(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    circle_boss.make_acceleration_up()
                if event.key == pygame.K_DOWN:
                    circle_boss.make_acceleration_down()
                if event.key == pygame.K_LEFT:
                    circle_boss.make_acceleration_left()
                if event.key == pygame.K_RIGHT:
                    circle_boss.make_acceleration_right()
        circle_boss.upgrade(dt, circle_other)
        screen.fill((0, 0, 0))  # black
        pygame.draw.circle(screen, circle_boss.color, circle_boss.get_coordinate(), circle_boss.radius)
        pygame.draw.circle(screen, circle_other.color, circle_other.get_coordinate(), circle_other.radius)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
