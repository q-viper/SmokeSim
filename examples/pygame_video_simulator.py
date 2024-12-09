import pygame_gui
import pygame
from smokesim.smoke import SmokeMachine, ParticleProperty
from pathlib import Path
import cv2
import numpy as np


def next_frame(cap, HEIGHT, WIDTH):
    ret, frame = cap.read()
    if ret:
        pass
    else:
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    screen_frame = cv2.resize(
        cv2.rotate(
            np.fliplr(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).astype(np.uint8),
            cv2.ROTATE_90_COUNTERCLOCKWISE,
        ),
        (HEIGHT, WIDTH),
    )
    bg = pygame.surfarray.make_surface(screen_frame)
    return bg, frame


def main():
    pygame.init()
    pygame.display.set_caption("Smoke Simulator")
    video_path = Path("media/vid.mp4")
    WIDTH, HEIGHT = 1000, 700
    save_dir = Path(r"\assets\generated")

    if not video_path.exists():
        raise ValueError(f"{video_path} not found.")
    else:
        cap = cv2.VideoCapture(str(video_path))
        bg, frame = next_frame(cap, HEIGHT, WIDTH)

    container_wh = (WIDTH, 150)
    screen = pygame.display.set_mode((WIDTH, HEIGHT + container_wh[1]))
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(bg, (0, container_wh[1]))

    manager = pygame_gui.UIManager((WIDTH, 150))
    color = (132, 136, 136)

    # Create a container for sliders, labels, and button
    container = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((0, 0), container_wh), manager=manager
    )

    # Increase width of elements by 50%
    slider_width = 150
    label_width = 200
    button_width = 150

    # Create horizontal sliders for RGB colors
    red_color_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((0, 0), (slider_width, 20)),
        start_value=color[0],
        value_range=(0, 255),
        manager=manager,
        container=container,
    )

    red_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, 20), (label_width, 20)),
        text="R",
        manager=manager,
        container=container,
    )

    green_color_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((slider_width + 10, 0), (slider_width, 20)),
        start_value=color[1],
        value_range=(0, 255),
        manager=manager,
        container=container,
    )

    green_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((slider_width + 10, 20), (label_width, 20)),
        text="G",
        manager=manager,
        container=container,
    )

    blue_color_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((2 * slider_width + 20, 0), (slider_width, 20)),
        start_value=color[2],
        value_range=(0, 255),
        manager=manager,
        container=container,
    )

    blue_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((2 * slider_width + 20, 20), (label_width, 20)),
        text="B",
        manager=manager,
        container=container,
    )

    max_life_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((3 * slider_width + 30, 0), (slider_width, 20)),
        start_value=8000,
        value_range=(1000, 10000),
        manager=manager,
        container=container,
    )

    max_life_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((3 * slider_width + 30, 20), (label_width, 20)),
        text="MaxLife: 8000",
        manager=manager,
        container=container,
    )

    max_particles_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((4 * slider_width + 40, 0), (slider_width, 20)),
        start_value=10,
        value_range=(1, 100),
        manager=manager,
        container=container,
    )

    max_particles_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((4 * slider_width + 40, 20), (label_width, 20)),
        text="MaxParticles: 5",
        manager=manager,
        container=container,
    )

    pause_video_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((5 * slider_width + 80, 0), (button_width, 40)),
        text="Pause Video",
        manager=manager,
        container=container,
    )

    min_vx_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((0, 40), (slider_width, 20)),
        start_value=0.9,
        value_range=(-2, 2),
        manager=manager,
        container=container,
    )

    min_vx_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, 60), (label_width, 20)),
        text="MinVx: 0.9",
        manager=manager,
        container=container,
    )

    min_vy_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((slider_width + 10, 40), (slider_width, 20)),
        start_value=-0.4,
        value_range=(-1, 1),
        manager=manager,
        container=container,
    )

    min_vy_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((slider_width + 10, 60), (label_width, 20)),
        text="MinVy: -0.4",
        manager=manager,
        container=container,
    )

    min_scale_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((2 * slider_width + 20, 40), (slider_width, 20)),
        start_value=10,
        value_range=(1, 30),
        manager=manager,
        container=container,
    )

    min_scale_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((2 * slider_width + 20, 60), (label_width, 20)),
        text="MinScale: 0",
        manager=manager,
        container=container,
    )

    min_life_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((3 * slider_width + 30, 40), (slider_width, 20)),
        start_value=2000,
        value_range=(1000, 10000),
        manager=manager,
        container=container,
    )

    min_life_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((3 * slider_width + 30, 60), (label_width, 20)),
        text="MinLife: 2000",
        manager=manager,
        container=container,
    )

    fade_speed = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((4 * slider_width + 40, 40), (slider_width, 20)),
        start_value=1,
        value_range=(1, 100),
        manager=manager,
        container=container,
    )

    fade_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((4 * slider_width + 40, 60), (label_width, 20)),
        text="Fade Speed: 100",
        manager=manager,
        container=container,
    )

    save_reference_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((5 * slider_width + 80, 40), (button_width, 40)),
        text="Save Reference",
        manager=manager,
        container=container,
    )

    max_vx_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((0, 80), (slider_width, 20)),
        start_value=0.04,
        value_range=(-1, 1),
        manager=manager,
        container=container,
    )

    max_vx_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, 100), (label_width, 20)),
        text="MaxVx: 0.04",
        manager=manager,
        container=container,
    )

    max_vy_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((slider_width + 10, 80), (slider_width, 20)),
        start_value=-0.1,
        value_range=(-1, 1),
        manager=manager,
        container=container,
    )

    max_vy_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((slider_width + 10, 100), (label_width, 20)),
        text="MaxVy: -0.1",
        manager=manager,
        container=container,
    )

    max_scale_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((2 * slider_width + 20, 80), (slider_width, 20)),
        start_value=100,
        value_range=(1, 100),
        manager=manager,
        container=container,
    )

    max_scale_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((2 * slider_width + 20, 100), (label_width, 20)),
        text="MaxScale: 100",
        manager=manager,
        container=container,
    )

    sprite_size_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((3 * slider_width + 30, 80), (slider_width, 20)),
        start_value=20,
        value_range=(15, 100),
        manager=manager,
        container=container,
    )

    sprite_size_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((3 * slider_width + 30, 100), (label_width, 20)),
        text="SpriteSize: 20",
        manager=manager,
        container=container,
    )

    save_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((4 * slider_width + 40, 80), (button_width, 40)),
        text="Save Smoke",
        manager=manager,
        container=container,
    )

    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((5 * slider_width + 80, 80), (button_width, 40)),
        text="Clear Smoke",
        manager=manager,
        container=container,
    )

    clock = pygame.time.Clock()
    running = True

    # Initialize SmokeMachine
    smoke_machine = SmokeMachine(
        screen, default_color=color, default_particle_count=5, default_sprite_size=25
    )
    smoke_machine.add_smoke(
        dict(particle_count=5, sprite_size=50, origin=(WIDTH // 2, HEIGHT))
    )
    particle_args = {}
    prev_mouse_pos = None
    steps = 0
    frame_number = 0

    pause_video = False
    ref_frame_number = None
    reference_frame = None
    while running:
        frame_number += 1
        steps += 1
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    print("Left mouse button clicked at:", event.pos)
                    if event.pos[1] > container_wh[1]:
                        smoke_machine.add_smoke(
                            dict(
                                color=smoke_machine.color,
                                particle_count=smoke_machine.particle_count,
                                sprite_size=smoke_machine.sprite_size,
                                origin=event.pos,
                                particle_args=particle_args,
                            )
                        )

                elif event.button == 3:  # Right mouse button
                    if event.pos[1] > container_wh[1]:
                        smoke_machine.smokes = []
                        smoke_machine.add_smoke(
                            dict(
                                color=smoke_machine.color,
                                particle_count=smoke_machine.particle_count,
                                sprite_size=smoke_machine.sprite_size,
                                origin=event.pos,
                                particle_args=particle_args,
                            )
                        )
                    print("Right mouse button clicked at:", event.pos)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == pause_video_button:
                    if not pause_video:
                        pause_video_button.set_text("Play Video")
                        pause_video = True
                    else:
                        pause_video = False
                        pause_video_button.set_text("Pause Video")
                if event.ui_element == save_button:
                    smoke_subsurface = screen.subsurface(
                        (0, container_wh[1], WIDTH, HEIGHT)
                    )
                    pygame.image.save(
                        smoke_subsurface,
                        str(save_dir / f"{video_path.stem}_{frame_number}_overlay.png"),
                    )
                    nbg = pygame.surfarray.make_surface(
                        np.zeros((WIDTH, HEIGHT + container_wh[1], 3), np.uint8)
                    )
                    smoke_machine.draw(nbg)
                    screen.blit(nbg, (0, 0))
                    smoke_subsurface = screen.subsurface(
                        (0, container_wh[1], WIDTH, HEIGHT)
                    )
                    pygame.image.save(
                        smoke_subsurface,
                        str(save_dir / f"{video_path.stem}_{frame_number}_mask.png"),
                    )

                    # smoke_machine.draw(bg)
                    screen.blit(bg, (0, container_wh[1]))
                    smoke_subsurface = screen.subsurface(
                        (0, container_wh[1], WIDTH, HEIGHT)
                    )
                    pygame.image.save(
                        smoke_subsurface,
                        str(save_dir / f"{video_path.stem}_{frame_number}_orig.png"),
                    )
                    if ref_frame_number:
                        cv2.imwrite(
                            str(
                                save_dir
                                / f"{video_path.stem}_{frame_number}_ref_{ref_frame_number}.png"
                            ),
                            cv2.cvtColor(reference_frame, cv2.COLOR_RGB2BGR),
                        )
                if event.ui_element == clear_button:
                    smoke_machine.empty()
                    steps = 0
                if event.ui_element == save_reference_button:
                    screen.blit(bg, (0, container_wh[1]))
                    smoke_subsurface = screen.subsurface(
                        (0, container_wh[1], WIDTH, HEIGHT)
                    )
                    reference_frame = pygame.surfarray.array3d(
                        pygame.transform.rotate(
                            pygame.transform.flip(smoke_subsurface, 0, 1), -90
                        )
                    )
                    ref_frame_number = frame_number

            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                smoke_machine.color = (
                    int(red_color_slider.get_current_value()),
                    int(green_color_slider.get_current_value()),
                    int(blue_color_slider.get_current_value()),
                )

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
                    "fade_speed": fade_speed.get_current_value(),
                }
                smoke_machine.particle_count = max_particles_slider.get_current_value()
                for smoke in smoke_machine.smokes:
                    smoke.particle_property = ParticleProperty(**particle_args)

                red_label.text = f"R: {smoke_machine.color[0]}"
                # red_label.text_colour = [smoke_machine.color[0], 0, 0]
                green_label.text = f"G: {smoke_machine.color[1]}"
                # green_label.text_colour = [0, smoke_machine.color[1], 0]
                blue_label.text = f"B: {smoke_machine.color[2]}"
                # blue_label.text_colour = [0, 0, smoke_machine.color[2]]

                max_particles_label.text = (
                    f"MaxParticles: {smoke_machine.particle_count}"
                )
                max_life_label.text = f"MaxLife: {particle_args['max_lifetime']}"
                min_life_label.text = f"MinLife: {particle_args['min_lifetime']}"
                fade_label.text = f"Fade: {particle_args['fade_speed']}"
                sprite_size_label.text = (
                    f"SpriteSize: {particle_args['smoke_sprite_size']}"
                )
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
                smoke_machine.add_smoke(
                    dict(
                        color=smoke_machine.color,
                        particle_count=1,
                        origin=mouse_pos,
                        lifetime=200,
                        particle_args={
                            "min_lifetime": 200,
                            "max_lifetime": 500,
                            "min_scale": 10,
                            "max_scale": 50,
                            "fade_speed": 50,
                            "scale": 50,
                            "smoke_sprite_size": 50,
                            "color": smoke_machine.color,
                        },
                    )
                )
        prev_mouse_pos = mouse_pos
        # Clear the screen
        # screen.fill((0, 0, 0))
        if not pause_video:
            bg, frame = next_frame(cap, HEIGHT, WIDTH)
        screen.blit(bg, (0, container_wh[1]))
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
