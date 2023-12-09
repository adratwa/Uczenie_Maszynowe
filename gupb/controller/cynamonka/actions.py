from gupb.controller.cynamonka.utils import POSSIBLE_ACTIONS
from gupb.controller.cynamonka.pathfinder import PathFinder
from gupb.model import characters
import random

class Actions:

    def __init__(self, knowledge, path_finder: PathFinder):
        self.my_knowledge = knowledge
        self.path_finder = path_finder

    # def go_in_the_target_direction(self, target_point):
    #             # Znajdź optymalną trasę do celu
    #     nearest_path_to_target = PathFinder.find_nearest_path(self.my_knowledge.map.walkable_area, self.my_knowledge.position, target_point)
        
    #     if nearest_path_to_target is not None and len(nearest_path_to_target) > 0:
    #         # Pobierz kierunek, w którym znajduje się kolejna pozycja na trasie
    #         next_position_direction = PathFinder.calculate_direction(self.my_knowledge.position, nearest_path_to_target[0])

    #         # Sprawdź, czy jesteśmy zwróceni w tym samym kierunku co kolejna pozycja
    #         if self.my_knowledge.facing.value == next_position_direction:
    #             # Jeśli tak, idź prosto
    #             return POSSIBLE_ACTIONS[2]
    #         else:
    #             # W przeciwnym razie, sprawdź, czy musimy obrócić się o 180 stopni
    #             if PathFinder.is_opposite_direction(self.my_knowledge.facing.value, next_position_direction):
    #                 return POSSIBLE_ACTIONS[1] #po prostu wtedy zawsze w prawo
    #             else:
    #                 # W przeciwnym razie, obróć się w kierunku kolejnej pozycji na trasie
    #                 return self.turn_towards_direction(next_position_direction)
    #     # Jeśli nie udało się znaleźć trasy, wykonaj losowy ruch
    #     return self.go_randomly()
    
    # def turn_towards_direction(self, target_direction):
    #     # Obróć się w kierunku podanego kierunku
    #     if self.my_knowledge.facing == characters.Facing.UP:
    #         if target_direction == characters.Facing.LEFT.value:
    #             return POSSIBLE_ACTIONS[0]  # Skręć w lewo
    #         else:
    #             return POSSIBLE_ACTIONS[1]  # Skręć w prawo
    #     elif self.my_knowledge.facing == characters.Facing.DOWN:
    #         if target_direction == characters.Facing.LEFT.value:
    #             return POSSIBLE_ACTIONS[1]  # Skręć w prawo                
    #         else:
    #             return POSSIBLE_ACTIONS[0]  # Skręć w lewo
    #     elif self.my_knowledge.facing == characters.Facing.LEFT:
    #         if target_direction == characters.Facing.UP.value:
    #             return POSSIBLE_ACTIONS[1]  # Skręć w prawo
    #         else:
    #             return POSSIBLE_ACTIONS[0]  # Skręć w lewo
    #     elif self.my_knowledge.facing == characters.Facing.RIGHT:
    #         if target_direction == characters.Facing.UP.value:
    #             return POSSIBLE_ACTIONS[0]  # Skręć w lewo
    #         else:
    #             return POSSIBLE_ACTIONS[1]  # Skręć w prawo
    #     else:
    #         return self.go_randomly()
        
    def go_randomly(self):
        print("go randomly")
        if self.my_knowledge.can_move_forward():
            return random.choices(POSSIBLE_ACTIONS[:3], [1,1,8], k=1)[0]
        elif self.my_knowledge.can_turn_right() and self.my_knowledge.can_turn_left():
            return random.choice(POSSIBLE_ACTIONS[5:])

        return random.choice(POSSIBLE_ACTIONS[:2])
        
    def go_in_menhir_direction(self, menhir_position):
        path_to_menhir, action = self.path_finder.calculate_next_move(menhir_position)
        if path_to_menhir and action:
            distance_from_menhir = len(path_to_menhir)
            if distance_from_menhir > 3:
                return action           
        return self.go_randomly()
    
    def go_to_center_of_map(self):
        print(f"go to center: {self.my_knowledge.map.center}")
        closest_point_to_center = PathFinder.find_the_closest_point_to_target(self.my_knowledge.map.walkable_area, self.my_knowledge.map.center)
        
        path_to_center, action = PathFinder.calculate_next_move( closest_point_to_center)
        if path_to_center and action:
            if len(path_to_center) > 3:
                return action
        return self.go_randomly()
    # def runaway_from_mist(self):
    #     # główne załozenie: jesli zidentyfikuje mgle na mapie kieruje sie w strone najdalszego odkrytego do tej pory punktu, do ktorego istenieje sciezka
    #     # Jeśli brak obszarów mgły, zwróć losową akcję
    #     if not self.mist_positions:
    #         return self.go_randomly()
        
    #     if self.runaway_target is not None and self.runaway_target not in self.walkable_area:

    #         max_distance = 0
    #         best_position = None

    #         for position in self.discovered_arena:
    #             if position not in self.mist_positions and position in self.walkable_area:
    #                 # Oblicz odległość między polem a najbliższym obszarem mgły
    #                 min_distance = min(math.dist(position, mist) for mist in self.mist_positions)

    #                 if min_distance > max_distance:
    #                     max_distance = min_distance
    #                     best_position = position

    #         if best_position is not None and self.find_nearest_path(self.walkable_area, self.position, best_position):
    #             # Znaleziono najlepsze pole, więc uciekaj w jego kierunku
    #             direction = coordinates.Coords(best_position[0] - self.position[0], best_position[1] - self.position[1])
    #             self.runaway_target = best_position
    #             return self.go_in_the_target_direction(self.runaway_target)
    #         else:
    #             # Brak dostępnych pól, które nie są w obszarze mgły, zwróć losową akcję
    #             return self.go_randomly()
    #     else:
    #         return self.go_in_the_target_direction(self.runaway_target)
