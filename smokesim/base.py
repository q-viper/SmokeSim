from pydantic import BaseModel
import numpy as np


class BaseProperty(BaseModel):
    """
    Just to make sure same random states will be used everywhere.
    """

    random_seed: int = 1000

    class ConfigDict:
        arbitrary_types_allowed = True


class BaseSim:
    """
    Base class for simulation
    """

    def __init__(self, property: BaseProperty):
        self.property = property
        self.base_random_state = np.random.RandomState(property.random_seed)

    @property
    def random_state(self):
        # return np.random.RandomState(self.base_random_state.randint(0, 1000000))
        return self.base_random_state

    def float_in_range(self, start, end):
        return start + self.random_state.random() * (end - start)

    @staticmethod
    def update(self, **kwargs):
        raise NotImplementedError
