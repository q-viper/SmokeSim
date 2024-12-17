import logging
from smokesim.augmentation import Augmentation
import numpy as np
import pytest
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Log level to capture INFO, WARNING, ERROR, etc.
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define log format
    handlers=[logging.StreamHandler()],  # Log to the console
)


# Helper function to create and setup augmentation with smoke particles
def setup_augmentation(
    seed: int, width: int, height: int, random_state: np.random.RandomState
) -> Augmentation:
    logging.info(f"Setting up augmentation with seed {seed}.")
    # Initialize Augmentation object
    augmentation = Augmentation(
        image_path=None, screen_dim=(width, height), random_seed=seed
    )
    smoke_machine = augmentation.smoke_machine

    # Add some smoke particles
    logging.info("Adding initial smoke particles.")
    augmentation.add_smoke(
        dict(
            particle_count=15,
            lifetime=2000,
            sprite_size=25,
            origin=(250, 500),
            particle_args={
                "min_lifetime": 200,
                "max_lifetime": 1000,
                "min_scale": 10,
                "max_scale": 50,
                "fade_speed": 2,
                "scale": 50,
                "smoke_sprite_size": 50,
                "min_vx": -2,
                "max_vx": 2,
                "color": smoke_machine.color,
            },
        )
    )
    augmentation.add_smoke(
        dict(particle_count=15, lifetime=2000, sprite_size=25, origin=(450, 500))
    )

    # Add random smoke particles
    for _ in range(5):
        augmentation.add_smoke(
            dict(
                color=smoke_machine.color,
                particle_count=10,
                origin=(
                    random_state.randint(100, width),
                    random_state.randint(100, height),
                ),
                lifetime=2000,
                particle_args={
                    "min_lifetime": 200,
                    "max_lifetime": 1000,
                    "min_scale": 10,
                    "max_scale": 50,
                    "fade_speed": 2,
                    "scale": 50,
                    "smoke_sprite_size": 50,
                    "min_vx": -2,
                    "max_vx": 2,
                    "color": smoke_machine.color,
                },
            )
        )

    logging.info("Augmentation setup complete.")
    return augmentation


# Helper function to run augmentation and return final image and mask
def run_augmentation(augmentation: Augmentation, steps: int = 15):
    logging.info(f"Running augmentation for {steps} steps.")
    final_image, final_mask = augmentation.augment(steps=steps)
    logging.info("Augmentation complete.")
    return final_image, final_mask


# Helper function to validate images and masks
def validate_images_and_masks(
    final_image1, final_mask1, final_image2, final_mask2, are_images_equal: bool = True
):
    logging.info("Validating images and masks.")
    assert (
        np.array_equal(final_image1, final_image2) == are_images_equal
    ), "Images equality check failed"
    assert np.array_equal(final_mask1, final_mask2), "Masks are not equal"
    logging.info("Validation complete.")


def test_augmentation():
    WIDTH, HEIGHT = 700, 500

    # Test 1: Same Seed for Augmentation
    logging.info(
        "Test 1: Running augmentation with the same seed for two augmentations."
    )
    augmentation1 = setup_augmentation(
        seed=42, width=WIDTH, height=HEIGHT, random_state=np.random.RandomState(42)
    )
    final_image1, final_mask1 = run_augmentation(augmentation1)

    augmentation2 = setup_augmentation(
        seed=42, width=WIDTH, height=HEIGHT, random_state=np.random.RandomState(42)
    )
    final_image2, final_mask2 = run_augmentation(augmentation2)

    logging.info("Checking if same masked images are generated for the same seed.")
    validate_images_and_masks(final_image1, final_mask1, final_image2, final_mask2)

    # Test 2: Different Seed for Augmentation
    logging.info("Test 2: Running augmentation with different seed.")
    augmentation3 = setup_augmentation(
        seed=50, width=WIDTH, height=HEIGHT, random_state=np.random.RandomState(42)
    )
    final_image3, final_mask3 = run_augmentation(augmentation3)

    logging.info("Checking if same masked images are generated for different seed.")
    assert not np.array_equal(
        final_image2, final_image3
    ), "Images should not be equal for different seeds"
    assert not np.array_equal(
        final_mask2, final_mask3
    ), "Masks should not be equal for different seeds"

    # Test 3: Ensure that the random seed is applied correctly
    logging.info("Test 3: Checking if seeds are applied correctly.")
    assert (
        augmentation3.smoke_machine.smokes[0].property.random_seed == 50
    ), "Seed not applied correctly."
    assert (
        augmentation1.smoke_machine.smokes[0].property.random_seed == 42
    ), "Seed not applied correctly."

    logging.info("PASSED.")


if __name__ == "__main__":
    # Run the test with pytest for better integration
    logging.info("Starting test execution.")
    pytest.main()
    # test_augmentation()
    logging.info("Test execution complete.")
