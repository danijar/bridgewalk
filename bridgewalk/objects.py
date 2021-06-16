import numpy as np

from . import constants


class Object:

  def __init__(self, world, pos):
    self.world = world
    self.pos = np.array(pos)
    self.random = world.random
    self.health = 0

  @property
  def texture(self):
    raise 'unknown'

  @property
  def walkable(self):
    return constants.walkable

  def move(self, direction):
    direction = np.array(direction)
    target = self.pos + direction
    if self.is_free(target):
      self.world.move(self, target)
      return True
    return False

  def is_free(self, target, materials=None):
    materials = self.walkable if materials is None else materials
    material, obj = self.world[target]
    return obj is None and material in materials

  def distance(self, target):
    if hasattr(target, 'pos'):
      target = target.pos
    return np.abs(target - self.pos).sum()

  def toward(self, target, long_axis=True):
    if hasattr(target, 'pos'):
      target = target.pos
    offset = target - self.pos
    dists = np.abs(offset)
    if (dists[0] > dists[1] if long_axis else dists[0] <= dists[1]):
      return np.array((np.sign(offset[0]), 0))
    else:
      return np.array((0, np.sign(offset[1])))

  def random_dir(self):
    dirs = ((-1, 0), (+1, 0), (0, -1), (0, +1))
    return dirs[self.random.randint(0, len(dirs))]


class Player(Object):

  def __init__(self, world, pos):
    super().__init__(world, pos)
    self.facing = (0, 1)

  @property
  def texture(self):
    if self.world[self.pos][0] == 'water':
      return 'player-water'
    else:
      return 'player'
    # return {
    #     (-1, 0): 'player-left',
    #     (+1, 0): 'player-right',
    #     (0, -1): 'player-up',
    #     (0, +1): 'player-down',
    # }[tuple(self.facing)]

  @property
  def walkable(self):
    return constants.walkable

  def update(self, action):
    target = (self.pos[0] + self.facing[0], self.pos[1] + self.facing[1])
    material, obj = self.world[target]
    # When in water move randomly, with current moving left.
    if self.world[self.pos][0] == 'water':
      action = self.random.choice(
          [0, 1, 2, 3, 4], p=[0.2, 0.25, 0.15, 0.2, 0.2])
    action = constants.actions[action]
    if action == 'noop':
      pass
    elif action.startswith('move_'):
      self._move(action[len('move_'):])

  def _move(self, direction):
    dirs = dict(left=(-1, 0), right=(+1, 0), up=(0, -1), down=(0, +1))
    self.facing = dirs[direction]
    self.move(self.facing)
