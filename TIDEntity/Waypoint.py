from .Util import *
from enum import Enum
class Waypoint(Enum):
    WP1 = [
        { "func": "circle", "params": {
            "center": (200,200), "radius": 2, "width": 0
            }
        }, { "func": "aaline", "params": {
                    "start_pos":    math.Vector2(197, 190),
                    "end_pos":      math.Vector2(210, 203)  
            }
        }, {
                "func": "aaline", "params": {
                    "start_pos":    math.Vector2(190, 197),
                    "end_pos":      math.Vector2(203, 210)  
                }
        }, { "func": "aalines", "params": {
            "closed":False, "points": [
                    math.Vector2(187, 207),
                    math.Vector2(187, 207) + math.Vector2.from_polar((14, mag(0)))
                ]
            }
        }
    ]
    DP =  [
        { "func": "circle", "params": {
                "center": (200,200), "radius": 2, "width": 0
            }
        }, { "func": "circle", "params": {
                "center": (200,200), "radius": 10, "width": 1 }
        }, { "func": "aaline", "params": {
                "start_pos":    math.Vector2(190, 190),
                "end_pos":      math.Vector2(210, 210)  
            }
        }
    ]


