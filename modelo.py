from manim import *


class MyStar(VMobject):
    CONFIG = {
        "start_time": 0,
        "frequency": .25,
        "max_ratio_shown": 2,
        "use_copy": True
    }

    def __init__(self, template, **kwargs):
        VMobject.__init__(self, **kwargs)
        if self.CONFIG['use_copy']:
            self.ghost_mob = template.copy().fade(1)
            self.add(self.ghost_mob)
        else:
            self.ghost_mob = template
        self.shown_mob = template.deepcopy()
        self.shown_mob.clear_updaters()
        self.add(self.shown_mob)
        self.total_time = self.CONFIG['start_time']

        def update(mob, dt):
            mob.total_time += dt
            period = 1/mob.CONFIG['frequency']
            # es importante la / para que el moviemietno de los hases sea perpetuo
            unsmooth_alpha = (mob.total_time % period)/period
            alpha = unsmooth_alpha  # aca no puse el bezier
            mob.shown_mob.pointwise_become_partial(
                mob.ghost_mob,
                # que pasa si saco el maximo?
                max(interpolate(-mob.CONFIG['max_ratio_shown'], 1, alpha), 0),
                min(interpolate(0, 1+mob.CONFIG['max_ratio_shown'], alpha), 1)
            )
        self.add_updater(update)


class MyCurves(VMobject):
    CONFIG = {
        "cd_mob_config": {
            "frequency": .2,
            "max_ratio_shown": .3,
        },
        "n_end": 2,
        "n_layers": 10,
        "radius": 1,
        "colors": [YELLOW_A, YELLOW_E],
        "R": 5,
        "r": 3,
        "d": 5,
    }

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        lines = self.get_lines()
        self.add(*[MyStar(
            line, **self.CONFIG['cd_mob_config']
        )
            for line in lines
        ])
        self.randomize_times()

    def randomize_times(self):
        for submob in self.submobjects:
            if hasattr(submob, "total_time"):
                T = 1/submob.frequency
                submob.total_time = T*np.random.random()

    def get_lines(self):
        a = .2
        return VGroup(*[self.get_line(self.CONFIG['radius']*(1-a+2*a*np.random.random())) for x in range(self.CONFIG['n_layers'])])

    def get_line(self, r):
        return ParametricFunction(
            lambda t: r*np.array([
                (self.CONFIG['R']-self.CONFIG['r'])*np.cos(t)+self.d *
                np.cos((self.CONFIG['R']-self.CONFIG['r'])/self.CONFIG['r']*t),
                (self.CONFIG['R']-self.CONFIG['r'])*np.sin(t)-self.d *
                np.sin((self.CONFIG['R']-self.CONFIG['r'])/self.CONFIG['r']*t),
                0
            ]),
            t_min=-3*PI+np.random.random(),
            t_max=3*PI+np.random.random(),
            stroke_width=1.4,
            color=interpolate_color(*self.CONFIG['colors'], np.random.random())
        )


class MakeEffect(Scene):
    def construct(self):
        suceso = MyCurves().set_height(config['frame_height'])
        self.play(FadeIn(suceso))
        self.wait(20)
