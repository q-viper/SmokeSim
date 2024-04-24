# Smoke Generation
Just some experiments while I am learning about smoke generation and simulating things. Demo: [pages/index.html](https://q-viper.github.io/SmokeSim/pages/index.html). Just move cursor on **Right canvas to see smoke effect**. Video might not play on demo server. But smoke does :)

## Disclaimer
I am no expert in JS and this project uses modified version of following two projects:
* [pages/scripts/smoke.js](pages/scripts/smoke.js) from: [bijection/smoke.js](https://github.com/bijection/smoke.js/)
* [pages/scripts/processor.js](pages/scripts/processor.js) from: [processor.js](https://github.com/mdn/dom-examples/blob/main/canvas/chroma-keying/processor.js)

**Huuuuuuuuuuge credit goes to original authors.**

## Demo 
### JavaScript Version
* On rightmost panel where video is being re-played, we can perform hover, click action to see smoke movement.
* Tweaking UI elements also works.

![](assets/js_demo.png)

#### What to do?
1. Clone this.
2. Start a localhost server (on this dir) to avoid CORS Errors. I am using [server.py](server.py) taken from [here](https://gist.github.com/acdha/925e9ffc3d74ad59c3ea#file-simple_cors_server-py). 
3. Open http://localhost:8003/pages/index.html and see it for yourself.

### PyGame Version
* Left click to **add** new smoke.
* Right click to **clear and write** new smoke.
* Hover to see wind effect.


![](assets/py_demo.png)

#### What to do?
* Run `particle.py` and TADAAAAAAAAAA!

## Using this As Augmentation
![](assets/augmented_smoke.png)

* Make use of `augmentation.py`. Ex.

```python
from augmentation import Augmentation
import numpy as np

np.random.seed(100)
WIDTH, HEIGHT = 700, 500
augmentation = Augmentation(screen_dim=(WIDTH, HEIGHT))
smoke_machine = augmentation.smoke_machine
augmentation.add_smoke(dict(particle_count=15, sprite_size=25,
                            origin=(250, 500)))
augmentation.add_smoke(dict(particle_count=15, sprite_size=25,
                            origin=(450, 500)))

augmentation.agument(90)
for i in range(5):
    augmentation.add_smoke(dict(color=smoke_machine.color, particle_count=1,
                                origin=(np.random.randint(100, WIDTH), np.random.randint(100, HEIGHT)), lifetime=200,
                                particle_args={'min_lifetime': 200,
                                                'max_lifetime': 500,
                                                'min_scale': 10,
                                                'max_scale': 50,
                                                'fade_speed': 50,
                                                'scale': 50,
                                                'smoke_sprite_size': 50,
                                                'color': smoke_machine.color}))
augmentation.agument(10)
augmentation.save_as()
augmentation.end()

```



## To do
* Add collision effect.
* Add wind effect.
* Make it smooth.
