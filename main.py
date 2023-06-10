import random
import sys
import pygame
from math import acos, asin, pi, sin, cos
from itertools import compress


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





class Circle:

    boost_x: float = 0
    boost_y: float = 0
    def __init__(self, coordinate: Coordinate, sped_x: float, sped_y: float, color:tuple, radius: float, ):
        self.coordinate = coordinate
        self.sped_x = sped_x
        self.sped_y = sped_y
        self.color = color
        self.radius = radius


    def move(self, dt, polygon):
        self.sped_x += self.boost_x - (self.sped_x * polygon.resistance_coefficient)
        self.sped_y += self.boost_y - (self.sped_y * polygon.resistance_coefficient)
        self.coordinate.step_all(dt * self.sped_x, dt * self.sped_y)
        self.points = [(cos(angel / 360 * pi * 2) * self.radius + self.get_coordinate()[0],
                        sin(angel / 360 * pi * 2) * self.radius + self.get_coordinate()[1])
                       for angel in range(0, 360, 30)]

    def change_color(self):
        speed = self.get_sped()
        if speed < 512:
            self.color= (int(speed/2), self.color[1], self.color[2])
        else:
            self.color=(255, self.color[1], self.color[2])

    def get_coordinate(self):
        return self.coordinate.get_coordinate()

    def hit_wall(self,):
        if (self.coordinate.x - self.radius <= 0) or (self.coordinate.x + self.radius >= self.wall.width):
            self.sped_x = -self.sped_x
        if (self.coordinate.y - self.radius <= 0) or (self.coordinate.y + self.radius >= self.wall.height):
            self.sped_y = -self.sped_y

    def get_point_angel(self, other):
        result = [(((x_point - other.get_coordinate()[0]) ** 2 +
                  (y_point - other.get_coordinate()[1]) ** 2
                  ) ** 0.5 <= other.radius) for x_point, y_point in self.points]
        t = list(compress(range(len(result)), result))
        return t[0]*30 if len(t)>=1 else None

    def is_touch(self, other):
        return any([(((x_point - other.get_coordinate()[0]) ** 2 +
                    (y_point - other.get_coordinate()[1]) ** 2
                    ) ** 0.5 <= other.radius) for x_point, y_point in self.points])


    def set_boost_x(self, boost: float = 0):
        self.boost_x = boost

    def set_boost_y(self, boost: float = 0):
        self.boost_y = boost

    def get_sped(self):
        return (self.sped_x**2 + self.sped_y**2)**0.5

    def make_acceleration_up(self, boost: float = 3):
        self.boost_y = -boost

    def make_acceleration_down(self, boost: float = 3):
        self.boost_y = boost

    def make_acceleration_left(self, boost: float = 3):
        self.boost_x = -boost

    def make_acceleration_right(self, boost: float = 3):
        self.boost_x = boost



    def upgrade(self, dt, others=None):
        self.hit_wall()
        self.move(dt)

        if others:
            for other in others:
                if self.is_touch(other):
                    self.sped_y, other.sped_y = other.sped_y, self.sped_y
                    self.sped_x, other.sped_x = other.sped_x, self.sped_x

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.resistance_coefficient = float(3 / 512)
        self.circles = []

    def get_canvas(self):
        return self.width, self.height

    def hit_wall(self, circle:Circle):
        if (circle.coordinate.x - circle.radius <= 0) or (circle.coordinate.x + circle.radius >= self.width):
            circle.sped_x = -circle.sped_x
        if (circle.coordinate.y - circle.radius <= 0) or (circle.coordinate.y + circle.radius >= self.height):
            circle.sped_y = -circle.sped_y

    def upgrade(self, dt):
        for circle in self.circles:
            self.hit_wall(circle)
            circle.move(dt, self)
            circle.change_color()
            for other in self.circles:
                if circle.is_touch(other) and not(circle == other):
                    circle.sped_y, other.sped_y = other.sped_y, circle.sped_y
                    circle.sped_x, other.sped_x = other.sped_x, circle.sped_x
    def append(self, circle):
        self.circles.append(circle)

def main():
    print(f"[+] Start project")
    canvas = Canvas(width=500, height=500)
    screen = pygame.display.set_mode(canvas.get_canvas())
    pygame.display.set_caption('YAHOOOO')
    clock = pygame.time.Clock()
    print(f"[+] create canvas")
    coordinate = Coordinate(x=30, y=30)
    circle_boss = Circle(coordinate, sped_x=30, sped_y=30, color=(150, 10, 50), radius=20)
    canvas.append(circle_boss)
    while True:
        dt = clock.tick(50) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_coordinate = Coordinate(event.pos[0], event.pos[1])
                    canvas.append(Circle(new_coordinate, sped_x=0, sped_y=0,
                                         color=(0, random.randint(0, 255), random.randint(0, 255)),
                                         radius=20))
                    print(event.pos)
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

        canvas.upgrade(dt)
        screen.fill((0, 0, 0))  # black
        pygame.draw.circle(screen, circle_boss.color, circle_boss.get_coordinate(), circle_boss.radius)
        for circle in canvas.circles:
            pygame.draw.circle(screen, circle.color, circle.get_coordinate(), circle.radius)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
