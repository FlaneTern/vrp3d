from typing import List
from uuid import uuid1

import numpy as np

from item.box import Box
from item.item import Item
from warehouse.pallet import Pallet


"""
    position: position in warehouse, 
            imagine the pallete rack
            spaces, it has 3 position, the rack index (x),
            the rack column (y), and the rack row or height (z)  
"""
class Rack:
    def __init__(self, 
                 position: np.ndarray,
                 size: np.ndarray, 
                 max_weight: int, 
                 name: str, 
                 pallet_list: List[Pallet],):
        self.id = str(uuid1())
        self.name = name
        self.size = size
        self.position = position
        self.pallet_list: List[Pallet] = pallet_list
        self.max_weight = max_weight

    @property
    def weight(self):
        return sum([pallet.weight for pallet in self.pallet_list])
    
    def is_insert_to_pallet_feasible(self, pallet_i, ep_i, item:Item)-> bool:
        if item.weight + self.weight > self.max_weight:
            return False
        ep = self.pallet_list[pallet_i].ep_list[ep_i]
        return self.pallet_list[pallet_i].is_insert_feasible(ep.position, item)

    def insert_to_pallet(self, pallet_i, ep_i, item:Item):
        self.pallet_list[pallet_i].insert(ep_i, item)