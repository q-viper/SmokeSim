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


def test_age():
    WIDTH, HEIGHT = 100, 100

    augmentation = Augmentation(
        image_path=None, screen_dim=(WIDTH, HEIGHT), random_seed=42
    )
    augmentation.add_smoke(
        dict(
            particle_count=1,
            sprite_size=25,
            origin=(50, 50),
            particle_args=dict(lifetime=20),
        )
    )
    augmentation.augment(2, time_step=30)
    assert len(augmentation.smoke_machine.smokes) == 1
    # after 1st step there will be 2 particles and increases by 1 each step
    assert len(augmentation.smoke_machine.smokes[0].particles) == 3
    # default time is 30 so first particle and second particle should be dead because of lifetime 10
    assert not augmentation.smoke_machine.smokes[0].particles[0].is_alive
    assert not augmentation.smoke_machine.smokes[0].particles[1].is_alive
    # third particle should be alive because it is just created
    assert augmentation.smoke_machine.smokes[0].particles[2].is_alive
    # age of first particle should be 30 and second should be 30
    assert augmentation.smoke_machine.smokes[0].particles[2].age == 0
    assert augmentation.smoke_machine.smokes[0].particles[1].age == 30

    logging.info("PASSED.")


def test_position():
    WIDTH, HEIGHT = 100, 100

    augmentation = Augmentation(
        image_path=None, screen_dim=(WIDTH, HEIGHT), random_seed=42
    )
    augmentation.add_smoke(
        dict(
            particle_count=1,
            sprite_size=25,
            origin=(50, 50),
            particle_args=dict(lifetime=1000, startvy=5),
        )
    )
    augmentation.augment(2, time_step=50)
    # because of high velocity particle should be out of screen
    assert not augmentation.smoke_machine.smokes[0].particles[0].is_alive

    logging.info("PASSED.")


if __name__ == "__main__":
    # Run the test with pytest for better integration
    logging.info("Starting test execution.")
    pytest.main()
    # test_position()
    # test_age()

    logging.info("Test execution complete.")
