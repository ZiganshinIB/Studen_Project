import sys
import pygame




def main():
    print(f"[+] Start project")
    screen, clock = create_canvas()
    print(f"[+] create canvas")
    x = 30
    y = 30
    sped_x = 50
    sped_y = 50
    while True:
        dt = clock.tick(50) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                sys.exit()
        x += sped_x * dt
        y += sped_y * dt
        screen.fill((0, 0, 0))  # black
        pygame.draw.circle(screen, (150, 10, 50), (int(x), int(y)), 20) # screen (color) (point_x, point_y) radius
        pygame.display.flip()


def create_canvas():
    width = 500
    height = 500
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('YAHOOOO')
    clock = pygame.time.Clock()
    return screen, clock


if __name__ == "__main__":
    pygame.init()
    main()
