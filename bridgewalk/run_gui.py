import argparse

import imageio
try:
  import pygame
except ImportError:
  print('Please install the pygame package to use the GUI.')
  raise

import bridgewalk


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--seed', type=int, default=None)
  parser.add_argument('--view', type=int, nargs=2, default=(15, 15))
  parser.add_argument('--length', type=int, default=None)
  parser.add_argument('--health', type=int, default=5)
  parser.add_argument('--window', type=int, nargs=2, default=(800, 800))
  parser.add_argument('--record', type=str, default=None)
  parser.add_argument('--fps', type=int, default=5)
  args = parser.parse_args()

  keymap = {
      pygame.K_a: 'move_left',
      pygame.K_d: 'move_right',
      pygame.K_w: 'move_up',
      pygame.K_s: 'move_down',
  }
  print('Actions:')
  for key, action in keymap.items():
    print(f'  {pygame.key.name(key)}: {action}')

  env = bridgewalk.Env(args.view, args.window, args.length, args.seed)
  env.reset()
  duration = 0
  return_ = 0
  was_done = False
  if args.record:
    frames = []

  pygame.init()
  screen = pygame.display.set_mode(args.window)
  clock = pygame.time.Clock()
  running = True
  while running:

    action = None
    pygame.event.pump()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        running = False
      elif event.type == pygame.KEYDOWN and event.key in keymap.keys():
        action = keymap[event.key]
    if action is None:
      pressed = pygame.key.get_pressed()
      for key, action in keymap.items():
        if pressed[key]:
          break
      else:
        action = 'noop'

    messages = []
    obs, reward, done, info = env.step(env.action_names.index(action))
    if env._step > 0 and env._step % 100 == 0:
      messages.append(f'Time step: {env._step}')
    if reward:
      messages.append(f'Reward: {reward}')
      return_ += reward
    if done and not was_done:
      was_done = True
      messages.append('Episode done!')
    if messages:
      print('\n'.join(messages), sep='')

    duration += 1
    if args.record:
      frames.append(obs)
    surface = pygame.surfarray.make_surface(
        obs.transpose((1, 0, 2)))

    screen.blit(surface, (0, 0))
    pygame.display.flip()
    clock.tick(args.fps)

  pygame.quit()
  print('Duration:', duration)
  print('Return:', return_)
  if args.record:
    imageio.mimsave(args.record, frames)
    print('Saved', args.record)


if __name__ == '__main__':
  main()
