class Smoke:
    def __init__(
        self,
        origin: List = [100, 100],
        lifespan: int = 100,
        start_particles: int = 5,
    ):
        self.origin = origin
        self.lifespan = lifespan
        self.start_particles = start_particles
        self.particles: Optional[List[Particle]] = []
        self._time = 0
        self.is_alive = True
        self._startup()
    
    @property
    def num_particles(self):
        return len(self.particles)

    def _startup(self):
        for sp in range(self.start_particles):
            p = Particle(
                x=self.origin[0]+np.random.randint(-10, 10),
                y=self.origin[1]+np.random.randint(-10, 10),
                z=20,
                lifespan=np.random.randint(self.lifespan/2, self.lifespan),
                x_update=lambda x, t: x + np.random.choice([-1, 1, 0]),
                y_update=lambda x, t: x*np.sin((t+x)*np.pi/180),
                num_subparticles=np.random.randint(1,3),
                subparticles_every=np.random.randint(0,2))
            self.particles.append(p)

    def update(self):
        
        temp_particles = []
        if self.lifespan >= self._time:
            for particle in self.particles:
                res = particle.update()
                if len(res) > 0:
                    temp_particles.extend(res)
                if not particle.is_alive:
                    del particle
                else:
                    temp_particles.append(particle)
        else:
            self.is_alive = False
        self.particles = temp_particles
        self._time += 1
        return self.particles
