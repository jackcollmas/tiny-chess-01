# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/jackcollmas/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/jackcollmas/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

My entry for the [make.fun bounty "Build the strongest chess engine in 4 KB of Python"](https://make.fun/bounty/tiny-chess-01).

## The Engine

`main.py` is a chess engine that plays through the make.fun environment. Currently implements a baseline strategy that captures the most valuable piece available.

## Rules

- `main.py` must be ≤ 4,096 bytes as committed
- Python 3.13 standard library only
- Search to fixed depth or node count (no clock dependency)
- Deterministic play for replay verification

## Local Testing

With Docker and the makefun CLI:

```bash
makefun grade-local --kit <kit-path> --bot <repo-path> --driver docker
```

## License

MIT License - see LICENSE file
