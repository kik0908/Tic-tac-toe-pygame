from typing import Dict

import pygame

import game_objects


class SceneManager:
    def __init__(self, display):
        self.display = display
        self.__active_scene = None

    def new_scene(self, scene):
        self.__active_scene = scene

    def update(self, events):
        self.__active_scene.update(events)

    def render(self):
        self.__active_scene.render()

    def next_step(self, events):
        self.update(events)
        self.render()

    @property
    def scene(self):
        return self.__active_scene


class Scene:
    def __init__(self, display, scene_manager: SceneManager):
        self._display = display
        self.objects = []

        self.scene_manager = scene_manager

        self.callbacks = {}

    def callback(self, name, kwargs: Dict):
        self.callbacks.get(name)(**kwargs)

    def update(self, events):
        self.handling_events(events)

        for obj in self.objects:
            ans = obj.update()
            if ans is not None:
                self.callbacks.get(ans[0])(ans[1])

    def handling_events(self, events):
        pass

    def render(self):
        for obj in self.objects:
            obj.render(self._display)

    def add_obj(self, obj):
        self.objects.append(obj)

    @property
    def display(self):
        return self._display


class MainGame(Scene):
    def __init__(self, display, scene_manager):
        super().__init__(display, scene_manager)

        self.objects.append(game_objects.TicTacToeGrid((0, 0), 100, (3, 3), width=2, scene=self))

        self.callbacks.update([('player_win', self.__player_win)])

    def __player_win(self, char):
        _scene = MainGame(self._display, self.scene_manager)
        if char == 'x':
            _scene.add_obj(game_objects.Cross((450, 450), 20))
            self.scene_manager.new_scene(_scene)
        elif char == 'o':
            _scene.add_obj(game_objects.Circle((450, 450), 20))
            self.scene_manager.new_scene(_scene)
        else:
            self.scene_manager.new_scene(_scene)

    def handling_events(self, events):
        for event in events:
            for obj in self.objects:
                if obj.check_event(event):
                    obj.click(event)
            if event.type == pygame.QUIT:
                exit(0)
