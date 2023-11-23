from random import seed

from item.box import Box
from data.problem_generator import ProblemGenerator
from vns.saving import saving
from vns.repack import repack
from vns.route_dp import improve_tours_by_dp
from vrp3d.vrp3d import VRP3D

from data.parse_output import parse_output, parse_input
from data.database import Database


def run():
    Database.Initialize()
    

    depot_coords = []
    orders = []
    vehicle_lists = []
    kode_cabangs = []
    
    
    '''
    ProblemGenerator.initialize()

    depot_coords, orders, kode_cabangs = parse_input()

    vehicle_lists = []
    for i in range(len(depot_coords)):
        vehicle_list1 = ProblemGenerator.generate_random_vehicles(10)
        vehicle_lists.append(vehicle_list1)


    for i in range(1):
        kode_cabang, depot_coord1 = ProblemGenerator.get_random_depot()
        order_list1 = ProblemGenerator.generate_random_orders(9, 3, 10, kode_cabang)
        vehicle_list1 = ProblemGenerator.generate_random_vehicles(10)
        depot_coords.append(depot_coord1)
        orders.append(order_list1)
        vehicle_lists.append(vehicle_list1)
        kode_cabangs.append(kode_cabang)
    '''
    for i in range(1):
        kode_cabang, depot_coord1 = Database.random_depot()
        order_list1 = Database.random_orders(9, 3, 10, kode_cabang)
        Database.generate_available_vehicles(10)
        vehicle_list1 = Database.random_available_vehicles(10)
        depot_coords.append(depot_coord1)
        orders.append(order_list1)
        vehicle_lists.append(vehicle_list1)
        kode_cabangs.append(kode_cabang)
    
    

    #depot_coords, orders = parse_input()

    #depot_coords = [depot_coord1]
    #orders = [order_list]

    
    problems = []
    solutions = []
    
    for k in range(len(depot_coords)):
        depot_coord = depot_coords[k]
        order_list = orders[k]
        vehicle_list = vehicle_lists[k]
        cbox_type_list = Database.get_all_duses(100)
        cbox_type_list = sorted(cbox_type_list, key=lambda box: box.volume)    
        for i, order in enumerate(order_list):
            print("Packing order ",i," into cardboxes")
            order_list[i].pack_items_into_cardboard_boxes(cbox_type_list)

        problem = VRP3D(vehicle_list,
                        order_list,
                        depot_coord)
        print("START SOLUTION GENERATION")

                        
        solution = saving(problem)
        problem.reset(solution)
        
        solution = improve_tours_by_dp(solution, problem)
        problem.reset(solution)
        
        problems.append(problem)
        solutions.append(solution)

    parse_output(problems, solutions, depot_coords, kode_cabangs)


if __name__ == "__main__":
    seed(20)
    run()