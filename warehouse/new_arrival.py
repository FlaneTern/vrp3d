from uuid import uuid1

import numpy as np

from item.item import Item

class NewArrival(Item):
    def __init__(self,  
                 size: np.ndarray, 
                 name: str,
                 is_fast_moving: bool,
                 is_new:bool=False):
        id = str(uuid1())
        super().__init__(id, size, name)
        self.is_fast_moving = is_fast_moving
        self.weight = 10
        self.is_new = is_new