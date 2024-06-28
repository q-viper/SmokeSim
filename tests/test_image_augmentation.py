from smokesim.augmentation import Augmentation
import numpy as np

WIDTH, HEIGHT = 700, 500
augmentation = Augmentation(image_path=None, screen_dim=(WIDTH, HEIGHT))
smoke_machine = augmentation.smoke_machine
augmentation.add_smoke(dict(particle_count=15, sprite_size=25, origin=(250, 500)))
augmentation.add_smoke(dict(particle_count=15, sprite_size=25, origin=(450, 500)))
random_state = np.random.RandomState(42)

# final_image = augmentation.augment(steps=90, history_path=Path('media/smoke_history.mp4'))
final_image, final_mask = augmentation.augment(steps=90)
for i in range(5):
    augmentation.add_smoke(
        dict(
            color=smoke_machine.color,
            particle_count=1,
            origin=(
                random_state.randint(100, WIDTH),
                random_state.randint(100, HEIGHT),
            ),
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
final_image1, final_mask1 = augmentation.augment(steps=1)
# augmentation.save_as('assets/augmented_smoke_image.jpg')
augmentation.end()

augmentation = Augmentation(image_path=None, screen_dim=(WIDTH, HEIGHT))
smoke_machine = augmentation.smoke_machine
augmentation.add_smoke(dict(particle_count=15, sprite_size=25, origin=(250, 500)))
augmentation.add_smoke(dict(particle_count=15, sprite_size=25, origin=(450, 500)))
random_state = np.random.RandomState(42)

# final_image = augmentation.augment(steps=90, history_path=Path('media/smoke_history.mp4'))
final_image, final_mask = augmentation.augment(steps=90)
for i in range(5):
    augmentation.add_smoke(
        dict(
            color=smoke_machine.color,
            particle_count=1,
            origin=(
                random_state.randint(100, WIDTH),
                random_state.randint(100, HEIGHT),
            ),
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
final_image2, final_mask2 = augmentation.augment(steps=1)
# augmentation.save_as('assets/augmented_smoke_image2.jpg')
augmentation.end()

print("Checking if same masked images are generated for same seed.")
assert np.array_equal(final_image1, final_image2), "Images are not equal"
print("Checking if same masks are generated for same seed.")
assert np.array_equal(final_mask1, final_image2), "Masks are not equal"
print("PASSED. \n")
print("Checking if results are different for different seed.")

augmentation = Augmentation(image_path=None, screen_dim=(WIDTH, HEIGHT), random_seed=50)
smoke_machine = augmentation.smoke_machine
augmentation.add_smoke(dict(particle_count=15, sprite_size=25, origin=(250, 500)))
augmentation.add_smoke(dict(particle_count=15, sprite_size=25, origin=(450, 500)))
random_state = np.random.RandomState(42)

# final_image = augmentation.augment(steps=90, history_path=Path('media/smoke_history.mp4'))
final_image, _ = augmentation.augment(steps=90)
for i in range(5):
    augmentation.add_smoke(
        dict(
            color=smoke_machine.color,
            particle_count=1,
            origin=(
                random_state.randint(100, WIDTH),
                random_state.randint(100, HEIGHT),
            ),
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
final_image3, final_mask3 = augmentation.augment(steps=1)
# augmentation.save_as('assets/augmented_smoke_image2.jpg')
augmentation.end()


print("Checking if same masked images are generated for different seed.")
assert not np.array_equal(final_image2, final_image3), "Images are equal"
print("Checking if same masks are generated for different seed.")
assert not np.array_equal(final_mask2, final_mask3), "Masks are equal"
