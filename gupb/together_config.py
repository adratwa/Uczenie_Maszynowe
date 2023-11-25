from gupb.controller import alpha_gupb
from gupb.controller import ancymon
from gupb.controller import aragorn
from gupb.controller import ares
from gupb.controller import batman
from gupb.controller import bob
from gupb.controller import cynamonka
from gupb.controller import cynamonka_v2
from gupb.controller import cynamonka_v3
from gupb.controller import cynamonka_v4
from gupb.controller import cynamonka_v5
from gupb.controller import forrest_gump
from gupb.controller import frog
from gupb.controller import krombopulos
from gupb.controller import maly_konik
from gupb.controller import mongolek
from gupb.controller import pat_i_kot
from gupb.controller import random
from gupb.controller import roger
from gupb.controller import r2d2
from gupb.scripts import arena_generator

CONFIGURATION = {
    'arenas': arena_generator.generate_arenas(50, arena_generator.random_size_generator()),
    'controllers': [
        #alpha_gupb.AlphaGUPB("AlphaGUPB"),
        ancymon.AncymonController("Ancymon"),
        aragorn.AragornController("AragornController"),
        #ares.AresController("Nike"),
        bob.FSMBot(),
        #batman.BatmanHeuristicsController('Batman'),
        #cynamonka.CynamonkaController("Cynamonka"),
        #cynamonka_v2.CynamonkaController("Cynamonka2"),
        cynamonka_v3.CynamonkaController("Cynamonka3"),
        #cynamonka_v4.CynamonkaController("Cynamonka4"),
        cynamonka_v5.CynamonkaController("Cynamonka5"),
        #forrest_gump.ForrestGumpController("Forrest Gump"),
        #frog.FrogController('Frog'),
        krombopulos.KrombopulosMichaelController(),
        maly_konik.MalyKonik("LittlePonny"),
        #mongolek.Mongolek('Mongolek'),
        pat_i_kot.PatIKotController("Kot i Pat"),
        random.RandomController("Alice"),
        r2d2.RecklessRoamingDancingDruid("R2D2"),
        roger.Roger('1'),
    ],
    'start_balancing': False,
    'visualise': False,
    'show_sight': False,
    'runs_no': 1000,
}
