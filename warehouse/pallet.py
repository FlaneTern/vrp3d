from uuid import uuid1

import numpy as np

from item.box import Box

class Pallet(Box):
    def __init__(self,  
                 size: np.ndarray,
                 position: np.ndarray,
                 max_weight: int, 
                 name: str, 
                 support_alpha: float = 0.51, 
                 temperature: int = 0):
        id = str(uuid1())
        super().__init__(id,
                         size, 
                         max_weight, 
                         name, 
                         support_alpha, 
                         temperature,
                         False)
        self.position = position
        self.distance_to_door: float

    def compute_distance_to_door(self, rack_pos: np.ndarray, door_pos: np.ndarray, door_size: np.ndarray):
        door_mid = door_pos + door_size/2
        self_mid = rack_pos+self.position + self.size/2
        self.distance_to_door =  np.linalg.norm(self_mid-door_mid)