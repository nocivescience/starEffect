from manim import *
class Star(VMobject):
    CONFIG = {
        'start_time': 0,
        'frequency': .25,
        'max_ratio_shown': 2,
    }
    def __init__(self, template, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.shown_mob = template.copy()
        self.set_points_as_corners([3*LEFT,3*RIGHT])
        self.total_time = self.CONFIG['start_time']*np.random.random()
        self.total_time = self.CONFIG['start_time']
        def update(mob,dt):
            mob.total_time += dt*.1
            period = mob.CONFIG['frequency']
            unsmooth_alpha = (mob.total_time % period)/period
            alpha = unsmooth_alpha
            mob.pointwise_become_partial(
                mob.shown_mob,
                max(interpolate(-self.CONFIG['max_ratio_shown'], 1, alpha), 0),
                min(interpolate(0, 1+self.CONFIG['max_ratio_shown'], alpha), 1)
            )
        self.add_updater(update)
class SquareCurves(VMobject):
    CONFIG={
        'frequency':.2,
        'max_ratio_shown':.3,
    }
    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        lines = self.get_lines()
        self.add(*[
            Star(line) for line in lines
        ])
        self.randomize_times()
    def randomize_times(self):
        for submob in self.submobjects:
            if hasattr(submob, "total_time"):
                T = 1/self.CONFIG['frequency']
                submob.total_time = T*np.random.random()
    def get_lines(self):
        return VGroup(*[
            self.get_line(np.random.random()+2)
            for _ in range(10)
        ])
    def get_line(self,r):
        return ParametricFunction(
            lambda t: r*np.array([
                np.cos(t),
                np.sin(t),
                0
            ]),
            t_range=[0,TAU],
            
        )
class PrincipalScene(Scene):
    def construct(self):
        star = SquareCurves()
        self.add(star)
        self.wait(6)