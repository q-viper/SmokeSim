import numpy as np
from typing import Union, Tuple, Optional


class PerlinNoise:
    """
    https://en.wikipedia.org/wiki/Perlin_noise
    """

    def __init__(
        self,
        seed: Optional[int] = None,
        octaves: Union[int, Tuple[int, int]] = 1,
        persistence: Union[float, Tuple[float, float]] = 0.5,
        lacunarity: Union[float, Tuple[float, float]] = 2.0,
        falloff: Union[float, Tuple[float, float]] = 1.2,
        noise_dimension: int = 2,
    ):
        self.seed = seed or np.random.randint(0, 100)
        self.random_state = np.random.RandomState(self.seed)

        # Resolve parameters
        self.octaves = int(self._resolve_param(octaves))
        self.persistence = self._resolve_param(persistence)
        self.lacunarity = self._resolve_param(lacunarity)
        self.falloff = self._resolve_param(falloff)
        self.noise_dimension = noise_dimension

        self.gradients = {}

    def _resolve_param(self, value: Union[float, int, Tuple[float, float]]) -> float:
        """Helper function to resolve a parameter to a single value."""
        if isinstance(value, (tuple, list)) and len(value) == 2:
            return self.random_state.uniform(value[0], value[1])
        return value

    def _dot_grid_gradient(self, ix, iy, x, y):
        if (ix, iy) not in self.gradients:
            angle = self.random_state.uniform(0, 2 * np.pi)
            self.gradients[(ix, iy)] = (np.cos(angle), np.sin(angle))
        gradient = self.gradients[(ix, iy)]
        dx, dy = x - ix, y - iy
        return dx * gradient[0] + dy * gradient[1]

    def _dot_grid_gradient_3d(self, ix, iy, iz, x, y, z):
        if (ix, iy, iz) not in self.gradients:
            theta = self.random_state.uniform(0, 2 * np.pi)
            phi = self.random_state.uniform(0, np.pi)
            self.gradients[(ix, iy, iz)] = (
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                np.cos(phi),
            )
        gradient = self.gradients[(ix, iy, iz)]
        dx, dy, dz = x - ix, y - iy, z - iz
        return dx * gradient[0] + dy * gradient[1] + dz * gradient[2]

    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a, b, t):
        return a + t * (b - a)

    def noise(self, x, y, z=None):
        if z is None:
            # 2D noise
            x0, y0 = int(np.floor(x)), int(np.floor(y))
            x1, y1 = x0 + 1, y0 + 1

            sx, sy = self._fade(x - x0), self._fade(y - y0)

            n0 = self._dot_grid_gradient(x0, y0, x, y)
            n1 = self._dot_grid_gradient(x1, y0, x, y)
            ix0 = self._lerp(n0, n1, sx)

            n0 = self._dot_grid_gradient(x0, y1, x, y)
            n1 = self._dot_grid_gradient(x1, y1, x, y)
            ix1 = self._lerp(n0, n1, sx)

            return self._lerp(ix0, ix1, sy)
        else:
            # 3D noise
            x0, y0, z0 = int(np.floor(x)), int(np.floor(y)), int(np.floor(z))
            x1, y1, z1 = x0 + 1, y0 + 1, z0 + 1

            sx, sy, sz = self._fade(x - x0), self._fade(y - y0), self._fade(z - z0)

            n000 = self._dot_grid_gradient_3d(x0, y0, z0, x, y, z)
            n100 = self._dot_grid_gradient_3d(x1, y0, z0, x, y, z)
            n010 = self._dot_grid_gradient_3d(x0, y1, z0, x, y, z)
            n110 = self._dot_grid_gradient_3d(x1, y1, z0, x, y, z)
            n001 = self._dot_grid_gradient_3d(x0, y0, z1, x, y, z)
            n101 = self._dot_grid_gradient_3d(x1, y0, z1, x, y, z)
            n011 = self._dot_grid_gradient_3d(x0, y1, z1, x, y, z)
            n111 = self._dot_grid_gradient_3d(x1, y1, z1, x, y, z)

            ix00 = self._lerp(n000, n100, sx)
            ix10 = self._lerp(n010, n110, sx)
            ix01 = self._lerp(n001, n101, sx)
            ix11 = self._lerp(n011, n111, sx)

            iy0 = self._lerp(ix00, ix10, sy)
            iy1 = self._lerp(ix01, ix11, sy)

            return self._lerp(iy0, iy1, sz)

    def fractal_noise(self, x, y, z=None):
        total = 0
        frequency = 1
        amplitude = 1
        max_value = 0

        for _ in range(self.octaves):
            if z is None:
                total += self.noise(x * frequency, y * frequency) * amplitude
            else:
                total += (
                    self.noise(x * frequency, y * frequency, z * frequency) * amplitude
                )
            max_value += amplitude
            amplitude *= self.persistence
            frequency *= self.lacunarity

        return total / max_value

    def generate_cloud_mask(
        self,
        width: int,
        height: int,
        scale: Union[float, Tuple[float, float]] = 10,
        octaves: Optional[Union[int, Tuple[int, int]]] = None,
        persistence: Optional[Union[float, Tuple[float, float]]] = None,
        lacunarity: Optional[Union[float, Tuple[float, float]]] = None,
        falloff: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> np.ndarray:

        scale = self._resolve_param(scale)
        if octaves is not None:
            self.octaves = int(self._resolve_param(octaves))
        if persistence is not None:
            self.persistence = self._resolve_param(persistence)
        if lacunarity is not None:
            self.lacunarity = self._resolve_param(lacunarity)
        if falloff is not None:
            self.falloff = self._resolve_param(falloff) 

        print(
            f"Generating cloud mask with scale: {scale}, octaves: {self.octaves}, persistence: {self.persistence}, lacunarity: {self.lacunarity}, falloff: {self.falloff}"
        )

        cloud_mask = np.zeros((height, width), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                if self.noise_dimension == 2:
                    noise_value = self.fractal_noise(x / scale, y / scale)
                elif self.noise_dimension == 3:
                    noise_value = self.fractal_noise(
                        x / scale, y / scale, self.random_state.uniform(0, 1)
                    )
                else:
                    raise ValueError("noise_dimension must be 2 or 3")
                normalized_value = (noise_value + 1) / 2
                cloud_mask[y, x] = int(normalized_value * 255)

        center_x, center_y = width // 2, height // 2
        max_distance = np.sqrt(center_x**2 + center_y**2)
        for y in range(height):
            for x in range(width):
                distance_to_edge = max_distance - np.sqrt(
                    (x - center_x) ** 2 + (y - center_y) ** 2
                )
                edge_factor = max(0, distance_to_edge / max_distance) ** self.falloff
                cloud_mask[y, x] = int(cloud_mask[y, x] * edge_factor + 5)

        return cloud_mask.astype(np.uint8)
