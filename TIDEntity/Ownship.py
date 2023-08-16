from .Util import *

ORIGIN = math.Vector2(400, 400)

class Ownship(sprite.Sprite):
    def __init__(self, dic):
        super().__init__()
        self.alt = 0
        self.hdg = 0
        self.__dict__.update(dic)
        
        self.TID_RANGE_INDEX = 2
        self.TID_RANGE = TID_RANGE_VALUES[self.TID_RANGE_INDEX]
        
        self.EL_BARS_INDEX = 3
        self.EL_BARS = EL_BARS_VALUES[self.EL_BARS_INDEX]
        self.EL_CTR = 0
        self.EL_VERNIER = 0
        self.EL_TOTAL = self.EL_CTR + self.EL_VERNIER
        self.Hlim = min(99_000, floor((self.alt + ((self.TID_RANGE * 6000) * tan(radians(self.EL_TOTAL)+radians(self.EL_BARS / 2))))))
        self.Llim = max(0,  floor((self.alt + ((self.TID_RANGE * 6000) * tan(radians(self.EL_TOTAL)-radians(self.EL_BARS / 2))))))
        
        self.AZ_SCAN_INDEX = 1
        self.AZ_SCAN = AZ_SCAN_VALUES[self.AZ_SCAN_INDEX]
        self.AZ_CTR = 0
        
        self.image = Surface((800, 800), SRCALPHA, 32)
        self.rect = self.image.get_rect(center=(200, 390))
        
    def update(self):
        self.TID_RANGE = TID_RANGE_VALUES[self.TID_RANGE_INDEX]
        self.EL_BARS = EL_BARS_VALUES[self.EL_BARS_INDEX]
        self.AZ_SCAN = AZ_SCAN_VALUES[self.AZ_SCAN_INDEX]
        self.EL_TOTAL = self.EL_CTR + self.EL_VERNIER
        δ = radians(self.EL_TOTAL)
        β = radians(self.EL_BARS / 2)
        a = self.alt
        b = self.TID_RANGE * 6000
        self.Hlim = min(99_000, max(floor((a + (b * tan(δ+β)))), 0))
        self.Llim = max(0,  min(floor((a + (b * tan(δ-β)))), 99_000))
        
        
        SCALE = self.TID_RANGE
        self.image.fill((0,0,0,0))
        draw.circle(self.image, (0,255,0), ORIGIN, 10, 1)
        for i in range(0, 400, int(400/(SCALE/20))):
            draw.aaline(self.image, (0, 255, 0),
                           ORIGIN+math.Vector2.from_polar(((i * 2), mag(self.AZ_SCAN) + self.AZ_CTR)),
                           ORIGIN+math.Vector2.from_polar(((i * 2) + 400/(SCALE/20),
                           mag(self.AZ_SCAN)+self.AZ_CTR))
            )
            draw.aaline(self.image, (0, 255, 0),
                           ORIGIN+math.Vector2.from_polar(((i * 2), mag(-self.AZ_SCAN)+ self.AZ_CTR)),
                           ORIGIN+math.Vector2.from_polar(((i * 2) + 400/(SCALE/20),
                           mag(-self.AZ_SCAN)+self.AZ_CTR))
            )
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=math.Vector2(200, 390))
