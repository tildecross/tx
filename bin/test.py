#!/usr/bin/env python3

import os
import sys

# Include library directory
SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])
sys.path.insert(0, SCRIPT_PATH + "/../lib")
