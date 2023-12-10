from gupb.controller import keyboard
from gupb.controller import random
from gupb.controller import cynamonka

keyboard_controller = keyboard.KeyboardController()
cynamon = cynamonka.CynamonkaController("Cynamonka")
CONFIGURATION = {
    'arenas': [
        'ordinary_chaos'
    ],
    'controllers': [
        cynamonka.CynamonkaController("Cynamonka"),
        random.RandomController("Alice"),
        random.RandomController("Bob"),
        random.RandomController("Cecilia"),
        random.RandomController("Darius"),
    ],
    'start_balancing': False,
    'visualise': True,
    'show_sight': cynamon,
    'runs_no': 1,
    'profiling_metrics': [],
}
