# BridgeWalk

[![PyPI](https://img.shields.io/pypi/v/bridgewalk.svg)](https://pypi.python.org/pypi/bridgewalk/#history)

BridgeWalk is a partially-observed reinforcement learning environment with
dynamics of varying stochasticity. The player needs to walk along a bridge to
reach a goal location. When the player walks off the bridge into the water, the
current will move it randomly until it gets washed back on the shore. A good
agent in this environment avoids this stochastic trap. The implementation of
BridgeWalk is based on the [Crafter][crafter] environment.

![Bridge Walk Video](https://github.com/danijar/bridgewalk/raw/main/media/video.gif)

[crafter]: https://github.com/danijar/crafter

## Play Yourself

You can play the game yourself with an interactive window and keyboard input.
The mapping from keys to actions, health level, and inventory state are printed
to the terminal.

```sh
# Install with GUI
pip3 install 'bridgewalk[gui]'

# Start the game
bridgewalk

# Alternative way to start the game
python3 -m bridgewalk.run_gui
```

The following optional command line flags are available:

| Flag | Default | Description |
| :--- | :-----: | :---------- |
| `--window <width> <height>` | 800 800 | Window size in pixels, used as width and height. |
| `--fps <integer>` | 5 | How many times to update the environment per second. |
| `--record <filename>.mp4` | None | Record a video of the trajectory. |
| `--view <width> <height>` | 7 7 | The layout size in cells; determines view distance. |
| `--length <integer>` | None | Time limit for the episode. |
| `--seed <integer>` | None | Determines world generation and creatures. |

## Training Agents

Installation: `pip3 install -U bridgewalk`

The environment follows the [OpenAI Gym][gym] interface:

```py
import bridgewalk

env = bridgewalk.Env(seed=0)
obs = env.reset()
assert obs.shape == (64, 64, 3)

done = False
while not done:
  action = env.action_space.sample()
  obs, reward, done, info = env.step(action)
```

[gym]: https://github.com/openai/gym

## Environment Details

### Reward

A reward of +1 is given the first time in each episode when the agent reaches
the island at the end of the bridge.

### Termination

Episodes terminate after 250 steps.

### Observation Space

Each observation is an RGB image that shows a local view of the world around
the player, as well as the inventory state of the agent.

### Action Space

The action space is categorical. Each action is an integer index representing
one of the possible actions:

| Integer | Name | Description |
| :-----: | :--- | :---------- |
| 0 | `noop` | Do nothing. |
| 1 | `move_left` | Walk left. |
| 2 | `move_right` | Walk right. |
| 3 | `move_up` | Walk up. |
| 4 | `move_down` | Walk down. |

## Questions

Please [open an issue][issues] on Github.

[issues]: https://github.com/danijar/bridgewalk/issues
