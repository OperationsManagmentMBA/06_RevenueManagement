# Revenue Management - Interactive Presentation

An interactive teaching presentation on Revenue Management fundamentals, built with [Marimo](https://marimo.io/).

## Topics Covered

1. **Booking Limits** - Protecting capacity for high-value customers using the newsvendor model
2. **Overbooking** - Managing no-shows through strategic overselling
3. **Combining Both Levers** - The sequential heuristic for integrated revenue management

## Features

- Interactive sliders for exploring parameter sensitivity
- Real-time simulations comparing different policies
- Discovery-based learning with parallel pedagogical structure

## Running the Presentation

```bash
# Install dependencies
uv sync

# Run as slides
uv run marimo run revenue.py

# Or edit interactively
uv run marimo edit revenue.py
```

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

## Course Context

Part of the Operations Management MBA curriculum at Mannheim Business School.
