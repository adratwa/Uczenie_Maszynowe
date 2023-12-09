import heapq
import math
from gupb.model.coordinates import Coords
from gupb.controller.cynamonka.brain import MyKnowledge
from gupb.model import characters, coordinates
from gupb.controller.cynamonka.utils import DIRECTIONS
from gupb.model.characters.Action import STEP_RIGHT, STEP_LEFT, STEP_FORWARD, STEP_BACKWARD, TURN_RIGHT, TURN_LEFT

class PathFinder:
    def __init__(self, my_knowledge: MyKnowledge):
        self.my_knowledge = my_knowledge
        self.g_score = None
        self.g_score = None
        self.max_map_size = max(self.my_knowledge.map.size)
    
    @staticmethod
    def manhattan_length(coords: Coords) -> int:
        return abs(coords.x) + abs(coords.y)
    
    @staticmethod
    def find_shortest_path_from_list(paths):
        not_empty_paths = [path for path in paths if path is not None]  # Fixed the list comprehension
        if not not_empty_paths:
            return None  # Return None if the list is empty
        shortest_path = min(not_empty_paths, key=len)
        return shortest_path
    
    @staticmethod
    def calculate_direction(from_position, to_position):
        # Oblicz kierunek między dwiema pozycjami
        direction = Coords(to_position[0] - from_position[0], to_position[1] - from_position[1])
        return direction
    @staticmethod
    def is_opposite_direction(direction1, direction2):
        # Sprawdź, czy dwie koordynaty są przeciwne sobie
        return  direction1[0] == -direction2[0] and direction1[1] == -direction2[1]
    
    @staticmethod
    def calculate_distance(point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    
    @staticmethod
    def find_the_closest_point_to_target(list_of_points, point):
        closest_point = None
        min_distance = float('inf')  # Initialize with a large value

        # Iterate through the coordinates and find the closest point
        for coord in list_of_points:
            distance = PathFinder.calculate_distance(coord, point)
            if distance < min_distance:
                min_distance = distance
                closest_point = coord
        return closest_point

    def update_paths(self, start: Coords):
        open_set = [(0, start)]
        self.came_from = {}
        self.g_score = {Coords(row, col): float('inf') for row in range(self.max_map_size+1) for col in range(self.max_map_size+1)}
        self.g_score[start] = 0

        while open_set:
            _, current = heapq.heappop(open_set)

            for direction in DIRECTIONS:
                neighbor = current + direction
                if not self.is_move_valid(neighbor):
                    continue

                new_g_score = self.g_score[current] + 1

                if new_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = new_g_score
                    heapq.heappush(open_set, (new_g_score, neighbor))

    def is_move_valid(self, point):
        x, y = point
        if 0 <= x <= self.max_map_size and 0 <= y <= self.max_map_size:
            if point in self.my_knowledge.map.walkable_area and point not in self.my_knowledge.dangerous_tiles.keys():
                return True

    def reconstruct_path(self, current_point):
        path = [current_point]
        while current_point in self.came_from:
            current_point = self.came_from[current_point]
            path.insert(0, current_point)
        return path

    def calculate_path_length(self, end: Coords):
        path = self.reconstruct_path(end)

        return len(path) - 1 if path else float('inf')

    def next_move_action(self, path: list[Coords], fast_move: bool = False) -> characters.Action:
        start = self.my_knowledge.position

        if not path or len(path) < 2:
            return None

        next_move = path[1]
        move_vector = coordinates.sub_coords(next_move, start)
        facing = self.my_knowledge.facing.value

        if fast_move:
            if facing == Coords(1, 0):
                return self.get_action_for_vector(move_vector)
            elif facing == Coords(0, 1):
                return self.get_action_for_vector(move_vector)
            elif facing == Coords(-1, 0):
                return self.get_action_for_vector(move_vector)
            elif facing == Coords(0, -1):
                return self.get_action_for_vector(move_vector)

        sub = coordinates.sub_coords(facing, move_vector)

        if PathFinder.manhattan_length(sub) == 2:
            return TURN_RIGHT

        if sub.x == 0:
            return TURN_LEFT if sub.y * move_vector.y == 1 else TURN_RIGHT
        if sub.y == 0:
            return TURN_RIGHT if sub.x * move_vector.x == 1 else TURN_LEFT

        return STEP_FORWARD

    def get_action_for_vector(self, move_vector):
        if move_vector == Coords(1, 0):
            return STEP_FORWARD
        elif move_vector == Coords(0, 1):
            return STEP_RIGHT
        elif move_vector == Coords(-1, 0):
            return STEP_BACKWARD
        elif move_vector == Coords(0, -1):
            return STEP_LEFT

    def calculate_next_move(self, end: Coords):
        path = self.reconstruct_path(end)
        action = self.next_move_action(path)
        return action, path
    
    
