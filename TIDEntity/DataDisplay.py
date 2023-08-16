from .Util import *

class DataDisplay(sprite.Sprite):
    def __init__(self, position, label=None, context=None, datum=None, format=None, isSigned=False, isCoordinate=False ):
        sprite.Sprite.__init__(self)
        self.label = label
        if context:
            self.context = context
            self.datum = datum
            self.data = self.context.__dict__.get(self.datum)
        self.position = position
        self.signed = isSigned
        self.isCoordinate = isCoordinate
        self.format = format
        self.image = Surface([400,400], SRCALPHA, 32)
        self.font = font.SysFont('Courier New', 14, True, False)
        self.rect = self.image.get_rect(center=self.position)
        
    def update(self):
        if self.context:
            self.data = self.context.__dict__.get(self.datum)
        if self.label:
            fmt = self.label + ' ' + self.format
        if self.format:
            fmt = self.format
        else: 
            x = self.data
            fmt = f"%0{4 + (x < 0)}.1f"
        self.image.fill((0,0,0,0))
        s = self.font.render(fmt % self.data, True, (0,255,0))
        ctr = s.get_rect(center=(200,200))
        self.image.blit(s, ctr)
        self.image = self.image.convert_alpha()
         
