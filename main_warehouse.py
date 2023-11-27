from random import randint
from typing import List

from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel

from data.database import Database
from packing.warehouse_packing import put_items_in_room
from warehouse.room import Room
from warehouse.pallet import Pallet
from warehouse.rack import Rack
from warehouse.new_arrival import NewArrival


class WItemResponse(BaseModel):
    id:str
    name:str
    rack_id:str
    pallet_id:str
    pos:List[int]
    projected_pos:List[int]
    size:List[int]
    is_new:bool
    is_fast_moving:bool

class PalletResponse(BaseModel):
    id: str
    pos: List[int]
    projected_pos: List[int]
    size:int
    item_list:List[WItemResponse]

class RackResponse(BaseModel):
    id: str
    pos: List[int]
    size:int
    pallet_list:List[PalletResponse]

class RoomResponse(BaseModel):
    size: List[int]
    door_pos: List[int]
    door_size: List[int]
    rack_list: List[RackResponse]



def get_pallets()-> List[Pallet]:
    size = np.asanyarray([300, 60, 50], dtype=np.int32)
    position = np.asanyarray([0,0,0], dtype=np.int32)
    pallet_bot = Pallet(size=size,
                     position=position,
                     max_weight=3000,
                     name="Bottom Pallet")
    size = np.asanyarray([300, 60, 50], dtype=np.int32)
    position = np.asanyarray([0,0,60], dtype=np.int32)
    pallet_mid = Pallet(size=size,
                     position=position,
                     max_weight=3000,
                     name="Mid Pallet")
    size = np.asanyarray([300, 60, 50], dtype=np.int32)
    position = np.asanyarray([0,0,120], dtype=np.int32)
    pallet_top = Pallet(size=size,
                     position=position,
                     max_weight=3000,
                     name="Top Pallet")
    return [pallet_bot]
    

def get_racks()-> List[Rack]:
    pos = np.asanyarray([550, 100, 0], dtype=np.int32)
    size = np.asanyarray([300, 60, 120], dtype=np.int32)
    rack_front_left = Rack(pos,
                            size,
                            100000,
                            name="Front Left",
                            pallet_list=get_pallets())
    pos = np.asanyarray([550, 300, 0], dtype=np.int32)
    size = np.asanyarray([300, 60, 120], dtype=np.int32)
    rack_front_mid_left = Rack(pos,
                            size,
                            100000,
                            name="Front Mid Left",
                            pallet_list=get_pallets())
    pos = np.asanyarray([550, 600, 0], dtype=np.int32)
    size = np.asanyarray([300, 60, 120], dtype=np.int32)
    rack_front_mid_right = Rack(pos,
                            size,
                            100000,
                            name="Front Mid Right",
                            pallet_list=get_pallets())
    pos = np.asanyarray([550, 800, 0], dtype=np.int32)
    size = np.asanyarray([300, 60, 120], dtype=np.int32)
    rack_front_right = Rack(pos,
                            size,
                            100000,
                            name="Front Right",
                            pallet_list=get_pallets())


    size = np.asanyarray([300, 60, 120], dtype=np.int32)
    pos = np.asanyarray([100, 100, 0], dtype=np.int32)
    rack_back_left = Rack(pos,
                            size,
                            100000,
                            name="Back Left",
                            pallet_list=get_pallets())
    pos = np.asanyarray([100, 300, 0], dtype=np.int32)
    size = np.asanyarray([300, 60, 120], dtype=np.int32)
    rack_back_mid_left = Rack(pos,
                            size,
                            100000,
                            name="Back Mid Left",
                            pallet_list=get_pallets())
    pos = np.asanyarray([100, 600, 0], dtype=np.int32)
    size = np.asanyarray([300, 60, 120], dtype=np.int32)
    rack_back_mid_right = Rack(pos,
                            size,
                            100000,
                            name="Back Mid Right",
                            pallet_list=get_pallets())
    pos = np.asanyarray([100, 800, 0], dtype=np.int32)
    size = np.asanyarray([300, 60, 120], dtype=np.int32)
    rack_back_right = Rack(pos,
                            size,
                            100000,
                            name="Back Right",
                            pallet_list=get_pallets())
    return [rack_front_left, rack_front_mid_left, rack_front_mid_right, rack_front_right, rack_back_left, rack_back_mid_left, rack_back_mid_right, rack_back_right]

def setup_warehouse()-> Room:
    rack_list = get_racks()
    return Room(rack_list)

# app = FastAPI()

# @app.post("/warehouse")
# async def simulate_warehouse():
if __name__ == '__main__':
    room = setup_warehouse()
    Database.Initialize()
    duses = Database.random_duses(100)
    new_arrival_list = [(NewArrival(dus.size, dus.name, randint(0,1))) for i,dus in enumerate(duses)]
    
    room, packed_items = put_items_in_room(room, new_arrival_list)
    # room.visualize()
    
    duses = Database.random_duses(50)
    new_arrival_list = [(NewArrival(dus.size, dus.name, randint(0,1), True)) for dus in duses]
    room, packed_items = put_items_in_room(room, new_arrival_list)
    
    room_json = room.to_json()
    with open("room.json", "a+") as f:
        f.write(room_json)
    # rack_list = []
    # for rack in room.rack_list:
    #     pallet_list = []
    #     for pallet in rack.pallet_list:
    #         item_list:List[WItemResponse] = []
    #         for item in pallet.packed_items:
    #             item_response = WItemResponse(item.id,
    #                                           item.name,
    #                                           rack.id,
    #                                           pallet.id,
    #                                           item.position.tolist(),
    #                                           (rack.position + pallet.position + item.position).tolist(),
    #                                           item.size.tolist(),
    #                                           item.is_new,
    #                                           item.is_fast_moving)
    #             item_list += [item_response]
    #         pallet_response = PalletResponse(pallet.id, 
    #                                         pallet.position.tolist(),
    #                                         (rack.position+pallet.position).tolist(),
    #                                         item_list)
    #         pallet_list += [pallet_response]
    #     rack_response = RackResponse(rack.id,
    #                                  rack.position.tolist(),
    #                                  pallet_list)
    #     rack_list += [rack_response]
    # room = RoomResponse(room.size.tolist(),
    #                     room.door_position.tolist(),
    #                     room.door_size.tolist(),
    #                     rack_list)
    # return room  