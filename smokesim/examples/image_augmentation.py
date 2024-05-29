from smokesim.augmentation import Augmentation

import numpy as np
from pathlib import Path

if __name__ == "__main__":
    np.random.seed(100)
    WIDTH, HEIGHT = 700, 500
    augmentation = Augmentation(image_path=None, screen_dim=(WIDTH, HEIGHT))
    smoke_machine = augmentation.smoke_machine
    augmentation.add_smoke(dict(particle_count=15, sprite_size=25, origin=(250, 500)))
    augmentation.add_smoke(dict(particle_count=15, sprite_size=25, origin=(450, 500)))

    augmentation.augment(steps=90,history_path=Path('media/smoke_history.mp4'))
    for i in range(5):
        augmentation.add_smoke(
            dict(
                color=smoke_machine.color,
                particle_count=1,
                origin=(np.random.randint(100, WIDTH), np.random.randint(100, HEIGHT)),
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
    augmentation.augment(steps=1)
    augmentation.save_as('assets/augmented_smoke_image.jpg')
    augmentation.end()
