import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
BLUE = (65, 105, 225)
RED = (204, 51, 51)
DARK_GREY = (169, 169, 169)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 35 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, name, x, y, radius, texture_path, mass, initial_velocity):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.texture_orig = pygame.image.load(texture_path).convert_alpha()
        self.texture = pygame.transform.scale(self.texture_orig, (2 * radius, 2 * radius))
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0  # Set initial velocities to 0
        self.y_vel = initial_velocity  # Assign initial velocity

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2 - self.radius
        y = self.y * self.SCALE + HEIGHT / 2 - self.radius
        win.blit(self.texture, (x, y))

        if not self.sun:
            distance_text = FONT.render(f"{self.name}: {round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x + self.radius, y + self.radius))

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

    def update_position(self, planets):
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


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 30, 'sun.png', 1.98892 * 10 ** 30, 0)
    sun.sun = True

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 4, 'mercury.png', 3.30 * 10 ** 23, -47.4 * 1000)
    venus = Planet("Venus", 0.723 * Planet.AU, 0, 7, 'venus.png', 4.8685 * 10 ** 24, -35.02 * 1000)
    earth = Planet("Earth", -1 * Planet.AU, 0, 8, 'earth.png', 5.9742 * 10 ** 24, 29.783 * 1000)
    mars = Planet("Mars", -1.524 * Planet.AU, 0, 6, 'mars.png', 6.39 * 10 ** 23, 24.077 * 1000)
    jupiter = Planet("Jupiter", 5.203 * Planet.AU, 0, 14, 'jupiter.png', 1.8982 * 10 ** 27, -13.07 * 1000)
    saturn = Planet("Saturn", 9.537 * Planet.AU, 0, 13, 'saturn.png', 5.6834 * 10 ** 26, -9.69 * 1000)
    uranus = Planet("Uranus", 19.191 * Planet.AU, 0, 10, 'uranus.png', 8.6810 * 10 ** 25, -6.81 * 1000)
    neptune = Planet("Neptune", 30.069 * Planet.AU, 0, 9, 'neptune.png', 1.02413 * 10 ** 26, -5.43 * 1000)

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
