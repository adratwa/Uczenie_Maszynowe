from .cynamonka_v5 import CynamonkaController
from gupb.model.arenas import ArenaDescription
__all__ = [
    'CynamonkaController5',
    'POTENTIAL_CONTROLLERS'
]
# TODO: tu chyba przed zrobieniem PR trzeba baedzie to zmeinic
POTENTIAL_CONTROLLERS = [
    CynamonkaController("CynamonkaController5"),
]
