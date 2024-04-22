import pygame_gui
import pygame
from smoke import SmokeMachine


def main():
    pygame.init()
    pygame.display.set_caption("Smoke Simulator")
    bg = pygame.image.load("assets/me.jpg")
    WIDTH, HEIGHT = 700, 500
    container_wh = (WIDTH, 150)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    # ui_screen = pygame.display.set_mode((WIDTH, 100))
    manager = pygame_gui.UIManager((WIDTH, 200))
    color = (24, 46, 48)
    # Create a container for sliders, labels, and button
    container = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), container_wh),
                                            manager=manager)

    # Create horizontal sliders for RGB colors
    red_color_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 0), (100, 20)),
                                                              start_value=color[0], value_range=(0, 255), manager=manager,
                                                              container=container)

    red_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 20), (50, 20)),
                                            text="R", manager=manager,
                                            container=container)
    green_color_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((110, 0), (100, 20)),
                                                                start_value=color[1], value_range=(0, 255), manager=manager,
                                                                container=container)

    green_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 20), (50, 20)),
                                              text="G", manager=manager,
                                              container=container)
    blue_color_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((220, 0), (100, 20)),
                                                               start_value=color[2], value_range=(0, 255), manager=manager,
                                                               container=container)
    blue_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((220, 20), (50, 20)),
                                             text="B", manager=manager,
                                             container=container)
    max_life_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((330, 0), (100, 20)),
                                                             start_value=8000, value_range=(1000, 10000), manager=manager,
                                                             container=container)
    max_life_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((330, 20), (100, 20)),
                                                 text="MaxLife: 8000", manager=manager,
                                                 container=container)
    max_particles_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((440, 0), (100, 20)),
                                                                  start_value=10, value_range=(1, 100), manager=manager,
                                                                  container=container)
    max_particles_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((440, 20), (100, 20)),
                                                      text="MaxParticles: 5", manager=manager,
                                                      container=container)
    min_vx_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 40), (100, 20)),
                                                           start_value=-0.04, value_range=(-2, 2), manager=manager,
                                                           container=container)
    min_vx_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 60), (100, 20)),
                                               text="MinVx: -0.04", manager=manager,
                                               container=container)
    min_vy_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((110, 40), (100, 20)),
                                                           start_value=-0.4, value_range=(-1, 1), manager=manager,
                                                           container=container)
    min_vy_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 60), (100, 20)),
                                               text="MinVy: -0.4", manager=manager,
                                               container=container)
    min_scale_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((220, 40), (100, 20)),
                                                              start_value=10, value_range=(1, 30), manager=manager,
                                                              container=container)
    min_scale_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((220, 60), (100, 20)),
                                                  text="MinScale: 0", manager=manager,
                                                  container=container)
    min_life_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((330, 40), (100, 20)),
                                                             start_value=2000, value_range=(1000, 10000), manager=manager,
                                                             container=container)
    min_life_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((330, 60), (100, 20)),
                                                 text="MinLife: 2000", manager=manager,
                                                 container=container)
    fade_speed = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((440, 40), (100, 20)),
                                                        start_value=1, value_range=(1, 100), manager=manager,
                                                        container=container)
    fade_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((440, 60), (100, 20)),
                                             text="Fade Speed: 100", manager=manager,
                                             container=container)
    max_vx_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, 80), (100, 20)),
                                                           start_value=0.04, value_range=(-1, 1), manager=manager,
                                                           container=container)
    max_vx_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 100), (100, 20)),
                                               text="MaxVx: 0.04", manager=manager,
                                               container=container)
    max_vy_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((110, 80), (100, 20)),
                                                           start_value=-0.1, value_range=(-1, 1), manager=manager,
                                                           container=container)
    max_vy_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 100), (100, 20)),
                                               text="MaxVy: -0.1", manager=manager,
                                               container=container)
    max_scale_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((220, 80), (100, 20)),
                                                              start_value=25, value_range=(1, 30), manager=manager,
                                                              container=container)
    max_scale_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((220, 100), (100, 20)),
                                                  text="MaxScale: 0.5", manager=manager,
                                                  container=container)
    sprite_size_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((330, 80), (100, 20)),
                                                                start_value=20, value_range=(15, 25), manager=manager,
                                                                container=container)
    sprite_size_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((330, 100), (100, 20)),
                                                    text="SpriteSize: 20", manager=manager,
                                                    container=container)

    save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((440, 80), (100, 40)),
                                               text="Save Smoke", manager=manager,
                                               container=container)
    clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 80), (100, 40)),
                                                text="Clear Smoke", manager=manager,
                                                container=container)

    clock = pygame.time.Clock()
    running = True

    # Initialize SmokeMachine
    smoke_machine = SmokeMachine(
        screen, default_color=color, default_particle_count=5, default_sprite_size=25)
    smoke_machine.add_smoke(dict(particle_count=5, sprite_size=50,
                                 origin=(WIDTH // 2, HEIGHT)))
    particle_args = {}
    prev_mouse_pos = None
    steps = 0
    while running:
        steps += 1
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    print("Left mouse button clicked at:", event.pos)
                    if event.pos[1] > container_wh[1]:
                        smoke_machine.add_smoke(dict(color=smoke_machine.color,
                                                     particle_count=smoke_machine.particle_count,
                                                     sprite_size=smoke_machine.sprite_size,
                                                     origin=event.pos,
                                                     particle_args=particle_args))

                elif event.button == 3:  # Right mouse button
                    if event.pos[1] > container_wh[1]:
                        smoke_machine.smokes = []
                        smoke_machine.add_smoke(dict(color=smoke_machine.color,
                                                     particle_count=smoke_machine.particle_count,
                                                     sprite_size=smoke_machine.sprite_size,
                                                     origin=event.pos,
                                                     particle_args=particle_args))
                    print("Right mouse button clicked at:", event.pos)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == save_button:
                    smoke_subsurface = screen.subsurface((0, container_wh[1],
                                                          WIDTH,
                                                          HEIGHT - container_wh[1]))
                    pygame.image.save(smoke_subsurface, f"smoke.png")
                if event.ui_element == clear_button:
                    smoke_machine.empty()
                    steps = 0

            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                smoke_machine.color = (int(red_color_slider.get_current_value()),
                                       int(green_color_slider.get_current_value()),
                                       int(blue_color_slider.get_current_value()))

                particle_args = {
                    "color": smoke_machine.color,
                    "min_vx": min_vx_slider.get_current_value(),
                    "max_vx": max_vx_slider.get_current_value(),
                    "min_vy": min_vy_slider.get_current_value(),
                    "max_vy": max_vy_slider.get_current_value(),
                    "min_scale": min_scale_slider.get_current_value(),
                    "max_scale": max_scale_slider.get_current_value(),
                    "min_lifetime": min_life_slider.get_current_value(),
                    "max_lifetime": max_life_slider.get_current_value(),
                    "smoke_sprite_size": sprite_size_slider.get_current_value(),
                    "fade_speed": fade_speed.get_current_value()
                }
                smoke_machine.particle_count = max_particles_slider.get_current_value()

                red_label.text = f"R: {smoke_machine.color[0]}"
                # red_label.text_colour = [smoke_machine.color[0], 0, 0]
                green_label.text = f"G: {smoke_machine.color[1]}"
                # green_label.text_colour = [0, smoke_machine.color[1], 0]
                blue_label.text = f"B: {smoke_machine.color[2]}"
                # blue_label.text_colour = [0, 0, smoke_machine.color[2]]

                max_particles_label.text = f"MaxParticles: {smoke_machine.particle_count}"
                max_life_label.text = f"MaxLife: {particle_args['max_lifetime']}"
                min_life_label.text = f"MinLife: {particle_args['min_lifetime']}"
                fade_label.text = f"Fade: {particle_args['fade_speed']}"
                sprite_size_label.text = f"SpriteSize: {particle_args['smoke_sprite_size']}"
                min_vx_label.text = f"MinVx: {particle_args['min_vx']}"
                max_vx_label.text = f"MaxVx: {particle_args['max_vx']}"
                min_vy_label.text = f"MinVy: {particle_args['min_vy']}"
                max_vy_label.text = f"MaxVy: {particle_args['max_vy']}"
                min_scale_label.text = f"MinScale: {particle_args['min_scale']}"
                max_scale_label.text = f"MaxScale: {particle_args['max_scale']}"

                red_label.rebuild()
                green_label.rebuild()
                blue_label.rebuild()
                max_particles_label.rebuild()
                max_life_label.rebuild()
                min_life_label.rebuild()
                fade_label.rebuild()
                sprite_size_label.rebuild()
                min_vx_label.rebuild()
                max_vx_label.rebuild()
                min_vy_label.rebuild()
                max_vy_label.rebuild()
                min_scale_label.rebuild()
                max_scale_label.rebuild()

            manager.process_events(event)

        manager.update(time_delta=clock.tick(60) / 1000.0)
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos != prev_mouse_pos:
            if mouse_pos[1] > container_wh[1] and mouse_pos[0] < WIDTH:
                print("Mouse position:", mouse_pos)
                smoke_machine.add_smoke(dict(color=smoke_machine.color, particle_count=1,
                                             origin=mouse_pos, lifetime=200,
                                             particle_args={'min_lifetime': 200,
                                                            'max_lifetime': 500,
                                                            'min_scale': 10,
                                                            'max_scale': 50,
                                                            'fade_speed': 50,
                                                            'scale': 50,
                                                            'smoke_sprite_size': 50,
                                                            'color': smoke_machine.color}))
        prev_mouse_pos = mouse_pos
        # Clear the screen
        # screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        for s in smoke_machine.smokes:
            print(f"Smoke id: {s.id}")
            print(f"Num particles: {len(s.particles)}")

        smoke_machine.update(clock.tick(60))

        # Draw UI elements
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()
    print(f"Ran for {steps} iterations")


main()
