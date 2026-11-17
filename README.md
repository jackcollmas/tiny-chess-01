# tiny-chess-01

My entry for the make.fun bounty "Build the strongest chess engine in 4 KB of Python".

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
