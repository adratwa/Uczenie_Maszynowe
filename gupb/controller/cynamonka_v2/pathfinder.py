import heapq
import math
from gupb.model.coordinates import Coords
from gupb.model import characters, coordinates
from gupb.controller.cynamonka.utils import DIRECTIONS


class PathFinder:
    def __init__(self, my_knowledge):
        self.my_knowledge = my_knowledge
        self.g_score = None
        self.came_from = None
        self.max_map_size = max(self.my_knowledge.map.size)
    
    @staticmethod
    def manhattan_length(coords: Coords) -> int:
        return abs(coords.x) + abs(coords.y)
    
    @staticmethod
    def find_shortest_path_from_list(paths):
        if not paths:
            return None  # Return None if the list is empty
        shortest_path = min(paths)
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
    
    @staticmethod
    def find_nearest_path( grid, start, goal):
        # Inicjalizuj listę odwiedzonych pozycji
        if goal is None:
            return None
        visited_positions = set()

        # Inicjalizuj kolejkę priorytetową do przechowywania pozycji i ich kosztów
        priority_queue = [(0, start, [])]  # (koszt, pozycja, ścieżka)

        while priority_queue:
            cost, current_position, path = heapq.heappop(priority_queue)

            if current_position == goal:
                return path  # Znaleziono cel, zwróć ścieżkę

            if current_position in visited_positions:
                continue  # Ta pozycja została już odwiedzona

            visited_positions.add(current_position)

            # Oblicz dostępne pozycje i ich koszty
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_position = (current_position[0] + dx, current_position[1] + dy)
                if new_position in grid:
                    new_cost = len(path) + 1 + math.dist(new_position, goal)
                    heapq.heappush(priority_queue, (new_cost, new_position, path + [new_position]))
        return None  # Nie znaleziono ścieżki do celu
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
            if point in self.my_knowledge.map.walkable_area:
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

    

    def next_move_action(self, path: list[Coords], fast_move: bool = False)-> characters.Action:
        start = self.my_knowledge.position
        facing_value = self.my_knowledge.facing.value
        if path and len(path) >= 3:
            if facing_value == Coords(1, 0):
                if self.my_knowledge.position + Coords(0, 1) == path[1] and self.my_knowledge.position + Coords(1,1) == path[2]:
                    return characters.Action.STEP_RIGHT
                if self.my_knowledge.position + Coords(0,-1) == path[1] and self.my_knowledge.position + Coords(1, -1) == path[2]:
                    return characters.Action.STEP_LEFT
            if facing_value == Coords(0, 1):
                if self.my_knowledge.position + Coords(1, 0) == path[1] and self.my_knowledge.position + Coords(1, 1) == path[2]:
                    return characters.Action.STEP_LEFT
                if self.my_knowledge.position + Coords(-1, 0) == path[1] and self.my_knowledge.position + Coords(-1, 1) == path[2]:
                    return characters.Action.STEP_RIGHT
            if facing_value == Coords(-1, 0):
                if self.my_knowledge.position + Coords(0,1) == path[1] and self.my_knowledge.position + Coords(-1,1) == path[2]:
                    return characters.Action.STEP_LEFT
                if self.my_knowledge.position + Coords(0,-1) == path[1] and self.my_knowledge.position + Coords(-1, -1) == path[2]:
                    return characters.Action.STEP_RIGHT
            if facing_value == Coords(0, -1):
                if self.my_knowledge.position + Coords(1, 0) == path[1] and self.my_knowledge.position + Coords(1, -1) == path[2]:
                    return characters.Action.STEP_RIGHT
                if self.my_knowledge.position + Coords(-1, 0) == path[1] and self.my_knowledge.position + Coords(-1, -1) == path[2]:
                    return characters.Action.STEP_LEFT

        if path and len(path) > 1 and fast_move:
            next_move = path[1]
            if not isinstance(next_move, Coords):
                next_move = Coords(next_move[0], next_move[1])
            if not isinstance(start, Coords):
                start = Coords(start[0], start[1])
            move_vector = next_move - start

            if facing_value == Coords(1, 0):
                if move_vector == Coords(1, 0):
                    return characters.Action.STEP_FORWARD
                if move_vector == Coords(0, 1):
                    return characters.Action.STEP_RIGHT
                if move_vector == Coords(-1, 0):
                    return characters.Action.STEP_BACKWARD
                if move_vector == Coords(0, -1):
                    return characters.Action.STEP_LEFT
            if facing_value == Coords(0, 1):
                if move_vector == Coords(1, 0):
                    return characters.Action.STEP_LEFT
                if move_vector == Coords(0, 1):
                    return characters.Action.STEP_FORWARD
                if move_vector == Coords(-1, 0):
                    return characters.Action.STEP_RIGHT
                if move_vector == Coords(0, -1):
                    return characters.Action.STEP_BACKWARD
            if facing_value == Coords(-1, 0):
                if move_vector == Coords(1, 0):
                    return characters.Action.STEP_BACKWARD
                if move_vector == Coords(0, 1):
                    return characters.Action.STEP_LEFT
                if move_vector == Coords(-1, 0):
                    return characters.Action.STEP_FORWARD
                if move_vector == Coords(0, -1):
                    return characters.Action.STEP_RIGHT
            if facing_value == Coords(0, -1):
                if move_vector == Coords(1, 0):
                    return characters.Action.STEP_RIGHT
                if move_vector == Coords(0, 1):
                    return characters.Action.STEP_BACKWARD
                if move_vector == Coords(-1, 0):
                    return characters.Action.STEP_LEFT
                if move_vector == Coords(0, -1):
                    return characters.Action.STEP_FORWARD

        if path and len(path) > 1:
            next_move = path[1]
            if not isinstance(next_move, Coords):
                next_move = Coords(next_move[0], next_move[1])
            if not isinstance(start, Coords):
                start = Coords(start[0], start[1])
            if not isinstance(facing_value, Coords):
                facing_value = Coords(facing_value[0], facing_value[1])
            move_vector = next_move - start
            sub = facing_value - move_vector

            if sub.x != 0 or sub.y != 0:
                if sub.x == 2 or sub.y == 2 or sub.x == -2 or sub.y == -2:
                    return characters.Action.TURN_RIGHT

                if move_vector.x == 0:
                    if sub.x * sub.y == 1:
                        return characters.Action.TURN_LEFT
                    else:
                        return characters.Action.TURN_RIGHT

                if move_vector.y == 0:
                    if sub.x * sub.y == 1:
                        return characters.Action.TURN_RIGHT
                    else:
                        return characters.Action.TURN_LEFT

            return characters.Action.STEP_FORWARD
        else:
            return None

    def calculate_next_move(self, end: Coords):
        path = self.reconstruct_path(end)
        action = self.next_move_action(path)
        return action, path
    
    
