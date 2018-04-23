# coding: utf-8

import os
import sys

# TODO remove for write demo base Scat witch in same dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == '__main__':
    os.environ.setdefault("SCAT_SETTINGS_MODULE", "TexasPoker.settings")
    try:
        from scat.commands import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions
        try:
            import scat
        except ImportError:
            raise ImportError(
                "Couldn't import scat. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line()
