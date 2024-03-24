

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from typing import List, Optional, Tuple

class Canvas:
    def __init__(
        self,
        background: List[int] = [1, 1, 1, 1],
        dimensions: List=(10, 20),
        shake_every: float=0,
        dpi: int = 100,
    ):
        self.background = background
        self.dimensions = dimensions
        self.shake_every = shake_every
        self._figure, self._axes = plt.subplots(figsize=dimensions, dpi=dpi, facecolor=background)
        self.scatter_points([[0.5,0.5]], [background], [0])
        self._frame = self.frame

    def scatter_points(self, points: List[List[int]], colors: List[List[int]], sizes: List[int]):
        for point,color,size in zip(points, colors, sizes):
            self._axes.scatter(point[0], point[1], color=color, s=size)
            self._axes.set_facecolor(self.background)
            self._axes.set_aspect('equal')
            
        self._figure.canvas.draw()
    
    
        
    @property
    def frame(self):
        return self._figure.canvas.renderer.buffer_rgba()      
        # return self._canvas.astype(np.uint8)
canvas = Canvas(background=[1, 1, 1], dimensions=(10, 10), dpi=50)

x_orig = 50
y_orig = 50
rad_orig = 500
x_update = lambda x, t: x+t #np.random.randomnp.random.choice([-1, 1, 0]) #np.sin(t*x)/(x*t)
y_update = lambda x,t: (x+t)*np.sin((x+t)*np.pi/180)#np.random.choice([-1, 1, 0]) #np.sin(t*x)/(x*t)
rad_update = lambda x,t: max(300, x-t) *np.random.random()# np.random.choice([-1, 1, 0]) #np.sin(t)
color_orig = [0.5, 0.5, 0.5, 0.8]
color_update = lambda x,t: x-x/t

pts = 500

coord = [(x_update(x_orig, i), y_update(y_orig, i)) for i in range(1, pts)]
rad = [rad_update(rad_orig, i) for i in range(1, pts)]
color = [[color_update(c, i) for c in color_orig] for i in range(1, pts)]
canvas.scatter_points(coord, color, rad)