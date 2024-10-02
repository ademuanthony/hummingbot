import os
import platform
from pathlib import Path


def app_data_dir(app_name: str, roaming: bool = False) -> str:
    """
    Returns an operating system-specific directory to store application data.

    :param app_name: The name of the application.
    :param roaming: Whether to use the roaming profile (Windows only).
    :return: The application data directory.
    """
    if not app_name or app_name == ".":
        return "."

    # Trim the period if the app_name starts with one
    app_name = app_name.lstrip('.')
    app_name_upper = app_name.capitalize()
    app_name_lower = app_name.lower()

    # Get the home directory
    home_dir = str(Path.home())

    # Check the operating system
    goos = platform.system().lower()

    if goos == "windows":
        # On Windows, prefer LOCALAPPDATA unless roaming is specified
        app_data = os.getenv("LOCALAPPDATA")
        if roaming or not app_data:
            app_data = os.getenv("APPDATA")

        if app_data:
            return os.path.join(app_data, app_name_upper)

    elif goos == "darwin":  # macOS
        if home_dir:
            return os.path.join(home_dir, "Library", "Application Support", app_name_upper)

    elif goos == "plan9":
        if home_dir:
            return os.path.join(home_dir, app_name_lower)

    else:  # POSIX (Linux, BSD, etc.)
        if home_dir:
            return os.path.join(home_dir, f".{app_name_lower}")

    # Fall back to the current directory if all else fails
    return "."
