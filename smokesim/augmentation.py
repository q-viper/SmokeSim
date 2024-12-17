from smokesim.smoke import SmokeMachine

import pygame
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
    ):

        self.image_path = image_path
        self.image = None
        self.screen_dim = screen_dim
        self.read_image(image_path)

        self.screen = smoke_machine.screen if smoke_machine else self.make_screen()
        self.smoke_machine = (
            smoke_machine
            if smoke_machine
            else SmokeMachine(self.screen, auto_draw=False, random_seed=random_seed)
        )
        self.smoke_machine.random_seed = random_seed
        self.display_image()

    def display_image(self):
        """
        A method to display the image on the screen.
        """
        if self.screen_dim == self.image.get_size():
            self.screen.blit(self.image, (0, 0))
        else:
            self.image = pygame.transform.scale(self.image, self.screen_dim)
        self.screen.blit(self.image, (0, 0))
        return self

    def read_image(self, image_path: Path) -> pygame.Surface:
        """
        A method to read an image.

        Args:
        - image_path (Path): The path to the image.

        Returns:
        - pygame.Surface: The image.
        """

        if image_path is not None:
            self.image = pygame.image.load(str(image_path))
            if not image_path.exists():
                Warning("No image path provided. Creating a blank image.")
                image_path = None
        if image_path is None:
            self.image = np.zeros((self.screen_dim[0], self.screen_dim[1], 3))

            self.image = pygame.surfarray.make_surface(self.image)

            self.image.set_alpha(255)

        self.image = pygame.transform.scale(self.image, self.screen_dim)
        blank_image = pygame.surfarray.make_surface(
            np.zeros((self.screen_dim[0], self.screen_dim[1], 3))
        )
        blank_image.set_alpha(255)
        self.blank_image = pygame.transform.scale(blank_image, self.screen_dim)

        return self

    def make_screen(self) -> pygame.Surface:
        """
        A method to make a screen.

        Returns:
        - pygame.Surface: The screen.
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        screen = pygame.display.set_mode(self.screen_dim, flags=pygame.HIDDEN)
        return screen

    def add_smoke(self, args: dict):
        """
        A method to add smoke to the screen.

        Args:
        - args (dict): The arguments to pass to the smoke machine.
        """
        self.smoke_machine.add_smoke(args)

    def augment_iter(
        self,
        steps: int,
        time_step: float,
        image: Optional[np.ndarray],
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
        """
        if image is not None:
            self.image = pygame.surfarray.make_surface(image)
            self.image = pygame.transform.scale(self.image, self.screen_dim)

        self.writer = None
        if history_path:
            self.writer = cv2.VideoWriter(
                str(history_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                30,
                self.image.get_size(),
            )
        for t in range(steps):
            # print(t)
            self.screen.blit(self.image, (0, 0))
            self.smoke_machine.update(time_step=time_step)
            self.smoke_machine.draw(self.screen)

            pygame.display.flip()
            rgb_array = pygame.surfarray.array3d(pygame.display.get_surface())
            if self.writer:
                self.writer.write(
                    cv2.cvtColor(
                        cv2.rotate(rgb_array, cv2.ROTATE_90_CLOCKWISE),
                        cv2.COLOR_RGB2BGR,
                    )
                )

            self.screen.blit(self.blank_image, (0, 0))
            self.smoke_machine.draw(self.screen)

            pygame.display.flip()
            rgb_mask_array = pygame.surfarray.array3d(pygame.display.get_surface())

            yield cv2.rotate(rgb_array, cv2.ROTATE_90_CLOCKWISE), cv2.rotate(
                rgb_mask_array, cv2.ROTATE_90_CLOCKWISE
            )

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
        ----------------
        - steps (int, optional): The number of steps to augment the image. Defaults to 2.
        - time_step (float, optional): The time step to augment the image. Defaults to 30.
        - image (Optional[np.ndarray], optional): The image to augment. Defaults to None.

        Returns:
        ----------------
        - np.ndarray: The smoke overlayed image.
        - np.ndarray: The smoke only image.
        """
        if image is not None:
            self.image = pygame.surfarray.make_surface(image)
            self.image = pygame.transform.scale(self.image, self.screen_dim)
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
        # pygame.image.save(self.screen, str(out_dir))
        cv2.imwrite(str(out_dir), cv2.cvtColor(self.last_aug_img, cv2.COLOR_RGB2BGR))
        cv2.imwrite(
            str(out_dir.parent / (out_dir.stem + "_mask.png")),
            cv2.cvtColor(self.last_aug_mask, cv2.COLOR_RGB2BGR),
        )
        print(f"Saved augmented image as {out_dir}")

    def end(self):
        """
        A method to end the pygame session.
        """
        pygame.quit()
