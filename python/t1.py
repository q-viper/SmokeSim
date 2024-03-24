# from GPT
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)
        self.color = (random.randint(100, 200),) * 3  # Grayish color
        self.alpha = 255  # Initial alpha value (fully opaque)
        self.fade_speed = random.randint(1, 5)  # Random fade speed
        self.vel_x = random.uniform(-1, 1)  # Random x velocity
        self.vel_y = random.uniform(-1, 1)  # Random y velocity

    def update(self):
        # Move particle
        self.x += self.vel_x
        self.y += self.vel_y
        # Fade out particle
        self.alpha -= self.fade_speed
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, screen):
        # Draw particle
        pygame.draw.circle(screen, (*self.color, self.alpha), (int(self.x), int(self.y)), self.size)


# Main function
def main():
    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smoke Simulation")

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # List to hold particles
    particles = []

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Create new particles
        for _ in range(10):
            particle = Particle(WIDTH // 2, HEIGHT)  # Start particles at the bottom center
            particles.append(particle)

        # Update and draw particles
        for particle in particles:
            particle.update()
            particle.draw(screen)

        # Remove faded-out particles
        particles = [p for p in particles if p.alpha > 0]

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
