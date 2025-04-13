from smokesim.augmentation import Augmentation
from smokesim.defs import SmokeProperty, ParticleProperty

import numpy as np
from pathlib import Path

if __name__ == "__main__":
    WIDTH, HEIGHT = 700, 500
    project_dir = Path(__file__).resolve().parents[1]
    img_path = project_dir / Path("assets/me.jpg")
    print(f"Image path: {img_path}")
    augmentation = Augmentation(image_path=img_path, screen_dim=(WIDTH, HEIGHT))
    smoke_machine = augmentation.smoke_machine
    smoke_properties = SmokeProperty(
        particle_count=15,
        sprite_size=25,
        origin=(250, 500),
    )
    augmentation.add_smoke(smoke_properties)
    smoke_properties = SmokeProperty(
        particle_count=15,
        sprite_size=25,
        origin=(450, 500),
    )
    augmentation.add_smoke(smoke_properties)
    random_state = np.random.RandomState(42)

    final_image = augmentation.augment(
        steps=90, history_path=project_dir / Path("media/smoke_history.mp4")
    )
    final_image, final_mask = augmentation.augment(steps=90)
    for i in range(5):
        smoke_properties = SmokeProperty(
            color=smoke_machine.color,
            particle_count=1,
            origin=(
                random_state.randint(100, WIDTH),
                random_state.randint(100, HEIGHT),
            ),
            lifetime=200,
            particle_property=ParticleProperty(
                min_lifetime=200,
                max_lifetime=500,
                min_scale=10,
                max_scale=50,
                fade_speed=50,
                scale=50,
                smoke_sprite_size=50,
                color=smoke_machine.color,
            ),
        )
        augmentation.add_smoke(
            smoke_property=smoke_properties,
        )
    final_image1, final_mask1 = augmentation.augment(steps=1)
    augmentation.save_as(project_dir / Path("assets/augmented_smoke_image.png"))
    augmentation.end()

    augmentation = Augmentation(image_path=img_path, screen_dim=(WIDTH, HEIGHT))
    smoke_machine = augmentation.smoke_machine
    smoke_properties = SmokeProperty(
        particle_count=15,
        sprite_size=25,
        origin=(250, 500),
    )
    augmentation.add_smoke(smoke_properties)
    smoke_properties = SmokeProperty(
        particle_count=15,
        sprite_size=25,
        origin=(450, 500),
    )
    augmentation.add_smoke(smoke_properties)
    random_state = np.random.RandomState(42)

    final_image = augmentation.augment(
        steps=90, history_path=project_dir / Path("media/smoke_history.mp4")
    )
    final_image, final_mask = augmentation.augment(steps=90)
    for i in range(5):
        smoke_properties = SmokeProperty(
            color=smoke_machine.color,
            particle_count=1,
            origin=(
                random_state.randint(100, WIDTH),
                random_state.randint(100, HEIGHT),
            ),
            lifetime=200,
            particle_property=ParticleProperty(
                min_lifetime=200,
                max_lifetime=500,
                min_scale=10,
                max_scale=50,
                fade_speed=50,
                scale=50,
                smoke_sprite_size=50,
                color=smoke_machine.color,
            ),
        )
        augmentation.add_smoke(
            smoke_property=smoke_properties,
        )
    final_image2, final_mask2 = augmentation.augment(steps=1)
    augmentation.save_as(project_dir / Path("assets/augmented_smoke_image.png"))
    augmentation.end()

    print(f"Are equal: {np.array_equal(final_image1, final_image2)}")
