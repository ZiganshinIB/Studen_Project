import sys
import pygame


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

    def get_canvas(self):
        return self.width, self.height


class Circle:
    def __init__(self, coordinate: Coordinate, sped_x: float, sped_y: float, color, radius: float):
        self.coordinate = coordinate
        self.sped_x = sped_x
        self.sped_y = sped_y
        self.color = color
        self.radius = radius

    def move(self, dt):
        self.coordinate.step_all(dt * self.sped_x, dt * self.sped_y)

    def get_coordinate(self):
        return self.coordinate.get_coordinate()

    def hit_wall(self, wall: Canvas):
        if (self.coordinate.x - self.radius <= 0) or (self.coordinate.x + self.radius >= wall.width):
            self.sped_x = -self.sped_x
        if (self.coordinate.y - self.radius <= 0) or (self.coordinate.y + self.radius >= wall.height):
            self.sped_y = -self.sped_y

    def make_acceleration_up(self, boost: float = 10):
        self.sped_y -= boost

    def make_acceleration_down(self, boost: float = 10):
        self.sped_y += boost

    def make_acceleration_left(self, boost: float = 10):
        self.sped_x -= boost

    def make_acceleration_right(self, boost: float = 10):
        self.sped_x += boost

    def upgrade(self, canvas, dt):
        self.hit_wall(canvas)
        self.move(dt)


def main():
    print(f"[+] Start project")
    canvas = Canvas(width=500, height=500)
    screen = pygame.display.set_mode(canvas.get_canvas())
    pygame.display.set_caption('YAHOOOO')
    clock = pygame.time.Clock()
    print(f"[+] create canvas")
    coordinate = Coordinate(x=30, y=30)
    circle_boss = Circle(coordinate, sped_x=50, sped_y=50, color=(150, 10, 50), radius=20)
    while True:
        dt = clock.tick(50) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    circle_boss.make_acceleration_up()
                if event.key == pygame.K_DOWN:
                    circle_boss.make_acceleration_down()
                if event.key == pygame.K_LEFT:
                    circle_boss.make_acceleration_left()
                if event.key == pygame.K_RIGHT:
                    circle_boss.make_acceleration_right()
        circle_boss.upgrade(canvas, dt)
        screen.fill((0, 0, 0))  # black
        pygame.draw.circle(screen, circle_boss.color, circle_boss.get_coordinate(), circle_boss.radius)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
