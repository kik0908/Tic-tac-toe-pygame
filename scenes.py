import pygame


class SceneManager:
    def __init__(self, scene, display):
        self.display = display
        self.active_scene = scene

    def new_scene(self, scene):
        self.active_scene = scene

    def update(self):
        self.active_scene.update()

    def render(self):
        self.active_scene.render()

    def next_step(self):
        self.update()
        self.render()


class Scene:
    def __init__(self, display):
        self.display = display

    def update(self):
        pass

    def render(self):
        pass


class MainGame(Scene):
    def __init__(self, display):
        super().__init__(display)

