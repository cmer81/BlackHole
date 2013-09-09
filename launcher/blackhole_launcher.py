#!/usr/bin/env python
import warnings
warnings.simplefilter("ignore")
import os
import sys
sys.path.append('/opt/BlackHole/')
from blackhole.black_hole_engine import BlackHole
from blackhole.black_hole_engine.gui import CursesMessage


def main():
    print("Loading...")
    try:
        SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blackhole.config')
        blackHole = BlackHole(SETTINGS_FILE)
        blackHole.main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        CursesMessage.msgBox(e.message)
        sys.exit(1)
        
if __name__ == '__main__':
    main() 
