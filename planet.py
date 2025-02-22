import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67429e-11
    SCALE = 180 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)
        return (x, y)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets, paused):
        if paused:
            return
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def draw_pause_button(win, paused):
    pygame.draw.rect(win, WHITE, (10, 10, 100, 40))
    font = pygame.font.Font(None, 30)
    text = font.render("Pause" if not paused else "Resume", True, BLACK)
    win.blit(text, (25, 20))

def main():
    run = True
    clock = pygame.time.Clock()
    paused = False
    font = pygame.font.Font(None, 30)

    sun = Planet(0, 0, 40, YELLOW, 1.98892 * 10**30, "Sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, "Mercury")
    mercury.y_vel = 47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]
    hovered_planet = None

    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        draw_pause_button(WIN, paused)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_planet = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= mouse_x <= 110 and 10 <= mouse_y <= 50:
                    paused = not paused

        for planet in planets:
            planet.update_position(planets, paused)
            px, py = planet.draw(WIN)
            if math.hypot(mouse_x - px, mouse_y - py) <= planet.radius:
                hovered_planet = planet

        if hovered_planet:
            text_surface = font.render(hovered_planet.name, True, WHITE, BLACK)
            WIN.blit(text_surface, (mouse_x + 10, mouse_y + 10))

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
