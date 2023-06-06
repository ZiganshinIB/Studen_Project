import sys
import pygame

width = 500
height = 500


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
    def __init__(self, coordinate: Coordinate, sped_x: float, sped_y: float, color, radius: float):
        self.coordinate = coordinate
        self.sped_x = sped_x
        self.sped_y = sped_y
        self.color = color
        self.radius = radius

    def move(self, dt):
        self.coordinate.step_all(dt*self.sped_x, dt*self.sped_y)

    def get_coordinate(self):
        return self.coordinate.get_coordinate()


def main():
    print(f"[+] Start project")
    screen, clock = create_canvas()
    print(f"[+] create canvas")
    coordinate = Coordinate(x=30, y=30)
    circle_boss = Circle(coordinate, sped_x=50, sped_y=50, color=(150, 10, 50), radius=20)
    while True:
        dt = clock.tick(50) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                sys.exit()
        circle_boss.move(dt)
        screen.fill((0, 0, 0))  # black
        pygame.draw.circle(screen, circle_boss.color, circle_boss.get_coordinate(), circle_boss.radius)
        pygame.display.flip()


def create_canvas():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('YAHOOOO')
    clock = pygame.time.Clock()
    return screen, clock


if __name__ == "__main__":
    pygame.init()
    main()
