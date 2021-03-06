MAP = """
..........................................................
..........................................................
..........................................................
..........................................................
..........................................................
..........................................................
......SSS.....BBBBBB................BBBBBB.....SSSS.......
.....STPPSS.BBB....BBB............BBB....BBB..SXXXTS......
.....SPPPPBBB........BBB........BBB........BBBBXCXXXS.....
......SPPPS............BBB....BBB.............SXXTXXS.....
.......SSS...............BBBBBB................SSXXS......
.................................................SS.......
..........................................................
..........................................................
..........................................................
..........................................................
..........................................................
"""


def generate_world(world, player):
  lines = MAP.split('\n')
  lines = [line.strip() for line in lines if line]
  spawns = []
  goals = []
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char == 'P':
        char = 'G'
        spawns.append((x, y))
      if char == 'X':
        char = 'G'
        goals.append((x, y))
      world[x, y] = {
          '.': 'water',
          'S': 'sand',
          'G': 'grass',
          'T': 'tree',
          'B': 'bridge',
          'C': 'crate',
          'X': 'goal',
      }[char]
  pos = spawns[world.random.randint(0, len(spawns))]
  world.move(player, pos)
  return goals
