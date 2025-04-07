import pytest
import numpy as np
from smokesim.noise import PerlinNoise


def test_2d_noise_randomness():
    """Test that 2D noise produces different values with different seeds."""
    noise1 = PerlinNoise(seed=42)
    noise2 = PerlinNoise(seed=43)

    value1 = noise1.noise(1.5, 2.5)
    value2 = noise2.noise(1.5, 2.5)

    assert value1 != value2, "2D noise values should differ with different seeds"


def test_3d_noise_randomness():
    """Test that 3D noise produces different values with different seeds."""
    noise1 = PerlinNoise(seed=42)
    noise2 = PerlinNoise(seed=43)

    value1 = noise1.noise(1.5, 2.5, 3.5)
    value2 = noise2.noise(1.5, 2.5, 3.5)

    assert value1 != value2, "3D noise values should differ with different seeds"


def test_fractal_noise_2d():
    """Test that fractal noise works for 2D."""
    noise = PerlinNoise(
        seed=42, octaves=(2, 4), persistence=(0.4, 0.6), lacunarity=(1.5, 2.0)
    )

    value = noise.fractal_noise(1.5, 2.5)

    assert isinstance(value, float), "Fractal noise should return a float value"
    assert -1.0 <= value <= 1.0, "Fractal noise value should be in the range [-1, 1]"


def test_fractal_noise_3d():
    """Test that fractal noise works for 3D."""
    noise = PerlinNoise(
        seed=42, octaves=(2, 4), persistence=(0.4, 0.6), lacunarity=(1.5, 2.0)
    )

    value = noise.fractal_noise(1.5, 2.5, 3.5)

    assert isinstance(value, float), "Fractal noise should return a float value"
    assert -1.0 <= value <= 1.0, "Fractal noise value should be in the range [-1, 1]"


def test_generate_cloud_mask():
    """Test that generate_cloud_mask produces consistent results with the same seed."""
    noise = PerlinNoise(
        seed=42,
        octaves=(2, 5),
        persistence=(0.4, 0.6),
        lacunarity=(1.5, 2.5),
        falloff=(1.0, 2.0),
        noise_dimension=2,
    )

    cloud_mask_1 = noise.generate_cloud_mask(width=20, height=20, scale=(5, 10))
    noise = PerlinNoise(
        seed=42,
        octaves=(2, 5),
        persistence=(0.4, 0.6),
        lacunarity=(1.5, 2.5),
        falloff=(1.0, 2.0),
        noise_dimension=2,
    )
    cloud_mask_2 = noise.generate_cloud_mask(width=20, height=20, scale=(5, 10))

    assert np.array_equal(
        cloud_mask_1, cloud_mask_2
    ), "Cloud masks should be identical with the same seed"


def test_generate_cloud_mask_random_state():
    """Test that generate_cloud_mask produces different results with different random states."""
    noise = PerlinNoise(
        seed=42,
        octaves=(2, 5),
        persistence=(0.4, 0.6),
        lacunarity=(1.5, 2.5),
        falloff=(1.0, 2.0),
        noise_dimension=2,
    )

    cloud_mask_1 = noise.generate_cloud_mask(width=20, height=20, scale=(5, 10))
    noise.random_state = np.random.RandomState(12345)  # Change random state
    cloud_mask_2 = noise.generate_cloud_mask(width=20, height=20, scale=(5, 10))

    assert not np.array_equal(
        cloud_mask_1, cloud_mask_2
    ), "Cloud masks should differ with different random states"
