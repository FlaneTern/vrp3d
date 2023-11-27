from copy import copy, deepcopy
from functools import cmp_to_key
from math import ceil
from typing import Dict, List, Tuple, NamedTuple

import numpy as np

from item.item import Item
from warehouse.rack import Rack
from warehouse.room import Room
from warehouse.pallet import Pallet
from warehouse.new_arrival import NewArrival


class InsertPosition(NamedTuple):
    rack: Rack
    pallet: Pallet

"""
sort item first by their packing order (LIFO),
if same order, then:
this sorting simply sort non-increasingly
by area, then height as tiebreaker also non-increasing
"""
def cmp_item_ah(item1:Item, item2:Item):
    if item1.packing_order < item2.packing_order:
        return -1
    if item1.packing_order > item2.packing_order:
        return 1
    if item1.face_area < item2.face_area:
        return 1
    if item1.face_area > item2.face_area:
        return -1
    if item1.size[2]< item2.size[2]:
        return -1
    if item1.size[2]> item2.size[2]:
        return 1
    return 0

def cmp_pallet_priority(ip1: InsertPosition, ip2: InsertPosition):
    if ip1.pallet.position[2]>ip2.pallet.position[2]:
        return 1
    if ip1.pallet.position[2]<ip2.pallet.position[2]:
        return -1
    if ip1.pallet.distance_to_door < ip2.pallet.distance_to_door:
        return -1
    if ip1.pallet.distance_to_door > ip2.pallet.distance_to_door:
        return 1
    if ip1.pallet.filled_volume > ip2.pallet.filled_volume:
        return -1
    if ip1.pallet.filled_volume < ip2.pallet.filled_volume:
        return 1
    return 0
    
def cmp_pallet_not_priority(ip1: InsertPosition, ip2: InsertPosition):
    if ip1.pallet.distance_to_door < ip2.pallet.distance_to_door:
        return 1
    if ip1.pallet.distance_to_door > ip2.pallet.distance_to_door:
        return -1
    if ip1.pallet.position[2]>ip2.pallet.position[2]:
        return 1
    if ip1.pallet.position[2]<ip2.pallet.position[2]:
        return -1
    if ip1.pallet.filled_volume > ip2.pallet.filled_volume:
        return -1
    if ip1.pallet.filled_volume < ip2.pallet.filled_volume:
        return 1
    return 0
    

def find_first_ep(ip_list:List[InsertPosition], item:Item):
    for i, ip in enumerate(ip_list):
        for ei, ep in enumerate(ip.pallet.ep_list):
            if ip.rack.weight + item.weight > ip.rack.max_weight:
                continue
            if not ip.pallet.is_insert_feasible(ep, item):
                continue
            return i, ei
    return -1, -1


def put_items_in_room(room: Room,
        item_list: List[NewArrival]) -> Tuple[Room, List[NewArrival]]:
    
    dup_items: List[NewArrival] = []
    for i, item in enumerate(item_list):
        item_list[i].rotate_count = 0
        for r in range(6):
            new_item = deepcopy(item)
            new_item.rotate_count = r
            dup_items += [new_item]
    item_list = dup_items
    item_list = sorted(item_list, key=cmp_to_key(cmp_item_ah))
    
    ip_list: List[InsertPosition] = []
    for i, rack in enumerate(room.rack_list):
        for j, pallet in enumerate(rack.pallet_list):
            ip_list += [InsertPosition(rack, pallet)]

    packed_items: List[Item] = []
    while item_list:
        item = item_list[0]
        del item_list[0]
        if item.is_fast_moving:
            ip_list = sorted(ip_list, key=cmp_to_key(cmp_pallet_priority))
        else:
            ip_list = sorted(ip_list, key=cmp_to_key(cmp_pallet_not_priority))
        ip_i, ep_i = find_first_ep(ip_list, item)
        if ip_i == -1:
            continue
        ip_list[ip_i].pallet.insert(ep_i, item)
        packed_items += [item]
        for i in reversed(range(len(item_list))):
            if item_list[i].id == item.id:
                del item_list[i]
        
    return room, packed_items      


        
