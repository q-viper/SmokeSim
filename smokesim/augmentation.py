from smokesim.smoke import SmokeMachine
from smokesim.engine import EngineTypes, Engine
from smokesim.defs import SmokeProperty

from typing import Optional, Tuple
from pathlib import Path
import numpy as np
import cv2


class Augmentation:
    def __init__(
        self,
        image_path: Optional[Path] = Path("assets/me.jpg"),
        screen_dim: Tuple[int, int] = (500, 700),
        smoke_machine: Optional[SmokeMachine] = None,
        random_seed: int = 100,
        engine_type: EngineTypes = EngineTypes.PYGAME,
    ):
        """
        Initialize the Augmentation class.

        Args:
        - image_path (Optional[Path], optional): The path to the image. Defaults to Path('assets/me.jpg').
        - screen_dim (Tuple[int, int], optional): The screen dimensions. Defaults to (500, 700).
        - smoke_machine (Optional[SmokeMachine], optional): The smoke machine. Defaults to None.
        - random_seed (int, optional): The random seed. Defaults to 100.
        - engine_type (EngineTypes, optional): The engine type. Defaults to EngineTypes.PYGAME.
        """
        self.image_path = image_path
        self.screen_dim = screen_dim
        self.engine_type = engine_type
        self.engine = Engine(screen_dim, engine_type)

        # Read the image
        self.engine.read_image(image_path)
        self.image = self.engine.image  # Ensure the image is initialized

        # Create the screen
        self.screen = self.engine.make_screen(
            self.screen_dim
        )  # Ensure screen is initialized
        self.smoke_machine = (
            smoke_machine
            if smoke_machine
            else SmokeMachine(self.screen, random_seed=random_seed)
        )
        self.smoke_machine.random_seed = random_seed

        # Display the image
        self.display_image()

    def display_image(self):
        """
        A method to display the image on the screen.
        """
        self.engine.display_image(self.image)

    def read_image(self, image_path: Path):
        """
        A method to read an image.

        Args:
        - image_path (Path): The path to the image.
        """
        self.image = self.engine.read_image(image_path)

    def make_screen(self):
        """
        A method to make a screen.

        Returns:
        - The screen object.
        """
        return self.engine.make_screen(self.screen_dim)

    def add_smoke(self, smoke_property: SmokeProperty):
        """
        A method to add smoke to the screen.

        Args:
        - args (dict): The arguments to pass to the smoke machine.
        """
        self.smoke_machine.add_smoke(smoke_property)

    def augment_iter(
        self,
        steps: int,
        time_step: float,
        image: Optional[np.ndarray] = None,
        history_path: Optional[Path] = None,
    ):
        """
        A method to augment the image with smoke.

        Args:
        - steps (int): The number of steps to augment the image.
        - time_step (float): The time step to augment the image.
        - image (Optional[np.ndarray]): The image to augment.
        - history_path (Path): The path to save the history.

        Yields:
        - np.ndarray: The augmented image.
        - np.ndarray: The smoke mask (RGB image with black background).
        """
        if image is not None:
            self.image = self.engine.make_surface(image)

        self.writer = None
        if history_path:
            self.writer = cv2.VideoWriter(
                str(history_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                30,
                self.screen_dim,
            )

        for t in range(steps):
            # Draw the base image
            self.engine.blit(self.screen, self.image, (0, 0))

            # Update and draw smoke particles
            self.smoke_machine.update(time_step=time_step)
            self.smoke_machine.draw(self.screen, self.engine)

            # Extract the augmented image
            if self.engine_type == EngineTypes.PYGAME:
                self.engine.engine.display.flip()
                rgb_array = self.engine.engine.surfarray.array3d(self.screen)
                rgb_array = cv2.rotate(rgb_array, cv2.ROTATE_90_CLOCKWISE)
            elif self.engine_type == EngineTypes.PIL:
                rgb_array = np.array(self.screen)

            # Clear the screen to black and redraw only the smoke for the mask
            if self.engine_type == EngineTypes.PYGAME:
                self.screen.fill((0, 0, 0))  # Clear the screen to black
            elif self.engine_type == EngineTypes.PIL:
                self.screen = self.engine.make_screen(
                    self.screen_dim
                )  # Create a new black screen

            self.smoke_machine.draw(self.screen, self.engine)

            # Extract the mask as an RGB image
            if self.engine_type == EngineTypes.PYGAME:
                self.engine.engine.display.flip()
                rgb_mask_array = self.engine.engine.surfarray.array3d(self.screen)
                rgb_mask_array = cv2.rotate(rgb_mask_array, cv2.ROTATE_90_CLOCKWISE)
            elif self.engine_type == EngineTypes.PIL:
                rgb_mask_array = np.array(self.screen)

            # Save the mask to the video writer if enabled
            if self.writer:
                self.writer.write(cv2.cvtColor(rgb_mask_array, cv2.COLOR_RGB2BGR))

            # Yield the augmented image and mask
            yield rgb_array, rgb_mask_array

    def augment(
        self,
        steps: int = 2,
        time_step: float = 30,
        image: Optional[np.ndarray] = None,
        history_path: Optional[Path] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        A method to augment the image with smoke.

        Args:
        - steps (int, optional): The number of steps to augment the image. Defaults to 2.
        - time_step (float, optional): The time step to augment the image. Defaults to 30.
        - image (Optional[np.ndarray], optional): The image to augment. Defaults to None.

        Returns:
        - np.ndarray: The smoke overlayed image.
        - np.ndarray: The smoke only image.
        """
        if image is not None:
            self.image = self.engine.make_surface(image)
        for rgb_array, rgb_mask_array in self.augment_iter(
            steps, time_step, image, history_path=history_path
        ):
            pass
        if self.writer:
            self.writer.release()
        self.last_aug_img, self.last_aug_mask = rgb_array, rgb_mask_array
        return self.last_aug_img, self.last_aug_mask

    def save_as(self, out_dir: Path = Path("assets/augmented_smoke.png")):
        """
        A method to save the augmented image.

        Args:
        - out_dir (Path, optional): The output directory to save the image. Defaults to Path('assets/augmented_smoke.png').
        """
        cv2.imwrite(str(out_dir), cv2.cvtColor(self.last_aug_img, cv2.COLOR_RGB2BGR))
        cv2.imwrite(
            str(out_dir.parent / (out_dir.stem + "_mask.png")),
            cv2.cvtColor(self.last_aug_mask, cv2.COLOR_RGB2BGR),
        )
        print(f"Saved augmented image as {out_dir}")

    def end(self):
        """
        A method to end the session.
        """
        self.engine.end()
