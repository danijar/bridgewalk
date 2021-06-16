import numpy as np

from . import constants
from . import engine
from . import objects
from . import worldgen


class Env:

  def __init__(
      self, view=(15, 15), size=(64, 64), length=250, seed=None):
    view = np.array(view if hasattr(view, '__len__') else (view, view))
    size = np.array(size if hasattr(size, '__len__') else (size, size))
    unit = size // view
    self._size = size
    self._length = length
    self._seed = seed
    self._episode = 0
    self._world = engine.World((
        max([len(line) for line in worldgen.MAP.split('\n') if line]),
        len([line for line in worldgen.MAP.split('\n') if line])))
    self._textures = engine.Textures(constants.root / 'assets')
    self._view = engine.LocalView(self._world, self._textures, unit, view)
    self._border = (size - unit * view) // 2
    self._step = None
    self._player = None
    self._goals = None
    self._once = None

  @property
  def observation_space(self):
    return engine.BoxSpace(0, 255, tuple(self._size) + (3,), np.uint8)

  @property
  def action_space(self):
    return engine.DiscreteSpace(len(constants.actions))

  @property
  def action_names(self):
    return constants.actions

  def reset(self):
    self._step = 0
    self._episode += 1
    self._world.reset(seed=hash((self._seed, self._episode)) % 2 ** 32)
    self._player = objects.Player(self._world, (0, 0))
    self._world.add(self._player)
    self._goals = worldgen.generate_world(self._world, self._player)
    self._once = True
    return self._obs()

  def step(self, action):
    self._step += 1
    # Copy object list so new added objects are not updated right away.
    for obj in list(self._world.objects):
      if obj is self._player:
        obj.update(action)
      else:
        obj.update()
    obs = self._obs()
    reward = 0.0
    if self._once and tuple(self._player.pos) in self._goals:
      self._once = False
      reward = 1.0
    done = self._length and self._step >= self._length
    info = {'discount': 1.0}
    return obs, reward, done, info

  def render(self):
    canvas = np.zeros(tuple(self._size) + (3,), np.uint8)
    view = self._view(self._player)
    (x, y), (w, h) = self._border, view.shape[:2]
    canvas[x: x + w, y: y + h] = view
    return canvas.transpose((1, 0, 2))

  def _obs(self):
    return self.render()
