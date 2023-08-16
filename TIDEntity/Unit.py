#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .Util import *

ORIGIN = math.Vector2(200,200)

class Unit(sprite.Sprite):
    def __getattr__(self, attr):
        return self.__dict__[attr]
    def __init__(self, dic):
        sprite.Sprite.__init__(self)
        self.dolly_track = dotdict({"visible": False, "IFF":"FND"})
        self.ownship_track= dotdict({"visible": False, "IFF":"UNK"})
        deep_update(self.__dict__, dic)
        self.selected = False
        self.image = Surface([400, 400], SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.radius = 10
    def update(self, OWNSHIP):
        AZ_SCAN = OWNSHIP.AZ_SCAN
        AZ_CTR = OWNSHIP.AZ_CTR
        Hlim = OWNSHIP.Hlim
        Llim = OWNSHIP.Llim
        braa= BRAA(OWNSHIP, self)
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(center=OWN_AC+math.Vector2.from_polar((400/(OWNSHIP.TID_RANGE/(braa.rng)), mag(braa.brg-OWNSHIP.hdg))))
        if angle_diff(mag(braa.brg-OWNSHIP.hdg), mag(-AZ_SCAN)+AZ_CTR) < 0 < angle_diff(mag(braa.brg-OWNSHIP.hdg), mag(AZ_SCAN)+AZ_CTR):
            if Hlim > self.alt > Llim:
                self.ownship_track.visible = True
            else:
                self.ownship_track.visible = False
        else:
            self.ownship_track.visible = False
            
        if self.dolly_track.visible or self.ownship_track.visible:
            
            draw.circle(self.image, (0, 255, 0),
                           ORIGIN, 1, 0)
            r, phi = (math.Vector2.from_polar((OWNSHIP.spd, OWNSHIP.hdg))-math.Vector2.from_polar((self.spd, self.hdg))).as_polar()
            vel_vec = math.Vector2.from_polar((int(r * 0.1), phi))
            draw.aaline(self.image, (0, 255, 0),
                            ORIGIN,
                            ORIGIN+vel_vec)
            if self.dolly_track.visible:
                if self.dolly_track.IFF == "FND":
                    draw.circle(self.image, (0, 255, 0),
                            ORIGIN, 10, 1, False, False, True, True
                    )
                if self.dolly_track.IFF == "UNK":
                    draw.lines(self.image, (0,255, 0), False, [
                                        ORIGIN+math.Vector2.from_polar((10, 180)),
                                        ORIGIN+math.Vector2.from_polar((10, 180))+math.Vector2.from_polar((10, 90)),
                                        ORIGIN+math.Vector2.from_polar((9, 0))+math.Vector2.from_polar((10, 90)),
                                        ORIGIN+math.Vector2.from_polar((9, 0))
                    ])
                if self.dolly_track.IFF == "HST":
                    draw.lines(self.image, (0,255, 0), False, [
                                        ORIGIN+math.Vector2.from_polar((10, 180)),
                                        ORIGIN+math.Vector2.from_polar((10, 90)),
                                        ORIGIN+math.Vector2.from_polar((9, 0))
                    ])
            if self.ownship_track.visible:
                LINE_THICKNESS = [1, 2][self.selected]
                if self.ownship_track.IFF == "FND":
                    draw.circle(self.image, (0, 255, 0),
                            ORIGIN, 10, 1, True, True, False, False
                    )
                if self.ownship_track.IFF == "UNK":
                    draw.lines(self.image, (0,255, 0), False, [
                                        ORIGIN+math.Vector2.from_polar((10, 180)),
                                        ORIGIN+math.Vector2.from_polar((10, 180))+math.Vector2.from_polar((10, 270)),
                                        ORIGIN+math.Vector2.from_polar((9, 0))+math.Vector2.from_polar((10, 270)),
                                        ORIGIN+math.Vector2.from_polar((9, 0))
                    ], LINE_THICKNESS)
                if self.ownship_track.IFF == "HST":
                    draw.lines(self.image, (0,255, 0), False, [
                                        ORIGIN+math.Vector2.from_polar((10, 180)),
                                        ORIGIN+math.Vector2.from_polar((10, 270)),
                                        ORIGIN+math.Vector2.from_polar((9, 0))
                    ])
        self.image = self.image.convert_alpha()    

        

