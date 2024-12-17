import cv2
import numpy as np
from pathlib import Path
from PIL import Image


def overlay_smoke(
    image: np.ndarray, smoke: np.ndarray, alpha_factor: float = 0.5
) -> np.ndarray:
    """
    A function to overlay smoke on an image.

    Args:
    - image (np.ndarray): The background image (4 channels - BGRA).
    - smoke (np.ndarray): The smoke image (3 channels - BGR).
    - alpha_factor (float): A scaling factor for smoke transparency (0 to 1).

    Returns:
    - np.ndarray: The image with smoke overlayed.

    """
    # Convert smoke to grayscale for alpha calculation
    smoke_gray = cv2.cvtColor(smoke, cv2.COLOR_BGR2GRAY)

    # Normalize the grayscale image to create transparency
    smoke_alpha = cv2.normalize(
        smoke_gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX
    )
    smoke_alpha = (smoke_alpha * alpha_factor).astype(
        np.uint8
    )  # Adjust intensity with alpha factor

    # Add an alpha channel to the smoke image
    smoke_rgba = cv2.cvtColor(smoke, cv2.COLOR_BGR2BGRA)
    smoke_rgba[:, :, 3] = smoke_alpha  # Assign the calculated alpha channel

    # Convert the input image and smoke image to PIL for alpha composition
    pimg = Image.fromarray(image, "RGBA")
    psmoke = Image.fromarray(smoke_rgba, "RGBA")

    # Use alpha_composite to overlay smoke on the image
    pimg.alpha_composite(psmoke)

    return np.array(pimg)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    smoke_path = project_root / "assets/generated/vid_406_mask.png"
    image_path = project_root / "assets/me.jpg"

    # Load images: IMPORTANT to read as 24 bit smoke image
    smoke = cv2.imread(str(smoke_path), cv2.IMREAD_COLOR)
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)

    # Resize the images
    image = cv2.resize(image, (700, 500))
    smoke = cv2.resize(smoke, (image.shape[1], image.shape[0]))

    # Convert the image to BGRA (add alpha channel)
    image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Overlay smoke
    overlayed_image = overlay_smoke(image_bgra, smoke, alpha_factor=0.99)

    # Combine images for comparison
    compare_images = np.hstack(
        (image_bgra, cv2.cvtColor(smoke, cv2.COLOR_BGR2BGRA), overlayed_image)
    )

    # Display the images
    cv2.imshow("Overlayed Image", compare_images)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
