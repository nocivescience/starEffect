from manim import *
class Star(VMobject):
    CONFIG = {
        'start_time': 0,
    }
    def __init__(self, template, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.shown_mob = template.copy()
        self.set_points_as_corners([LEFT,RIGHT])
        self.total_time = self.CONFIG['start_time']
        def update(mob,dt):
            mob.total_time += dt*.1
            mob.move_to(mob.get_center()+np.array([0,-mob.total_time,0]))
        self.add_updater(update)
class PrincipalScene(Scene):
    def construct(self):
        star = Star(Square())
        self.add(star)
        self.wait(4)