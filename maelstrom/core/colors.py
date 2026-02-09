"""ANSI color codes and color helper."""

import sys


class Colors:
    """ANSI color codes for terminal output — Catppuccin Mocha palette."""

    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Core semantic colors (mapped from Catppuccin Mocha)
    GREEN = "\033[38;2;166;227;161m"  # #a6e3a1 - Green
    RED = "\033[38;2;243;139;168m"  # #f38ba8 - Red
    YELLOW = "\033[38;2;249;226;175m"  # #f9e2af - Yellow
    BLUE = "\033[38;2;137;180;250m"  # #89b4fa - Blue
    MAGENTA = "\033[38;2;203;166;247m"  # #cba6f7 - Mauve
    CYAN = "\033[38;2;116;199;236m"  # #74c7ec - Sapphire
    WHITE = "\033[38;2;205;214;244m"  # #cdd6f4 - Text

    # Extended Catppuccin Mocha palette
    PEACH = "\033[38;2;250;179;135m"  # #fab387
    TEAL = "\033[38;2;148;226;213m"  # #94e2d5
    SKY = "\033[38;2;137;220;235m"  # #89dceb
    LAVENDER = "\033[38;2;180;190;254m"  # #b4befe
    PINK = "\033[38;2;245;194;231m"  # #f5c2e7
    MAROON = "\033[38;2;235;160;172m"  # #eba0ac
    FLAMINGO = "\033[38;2;242;205;205m"  # #f2cdcd
    ROSEWATER = "\033[38;2;245;224;220m"  # #f5e0dc
    SUBTEXT = "\033[38;2;186;194;222m"  # #bac2de - Subtext1
    OVERLAY = "\033[38;2;147;153;178m"  # #9399b2 - Overlay2
    SURFACE = "\033[38;2;88;91;112m"  # #585b70 - Surface2


def supports_color():
    """Check if terminal supports color."""
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


USE_COLOR = supports_color()


def c(text: str, color: str) -> str:
    """Apply color to text if supported."""
    if USE_COLOR:
        return f"{color}{text}{Colors.RESET}"
    return text
