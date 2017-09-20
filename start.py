"""
Entry point for visioninabox.
Takes 2 parameters:
  - headless
  - config_dir
"""

import argparse
from vision import Vision

###################################
# Get arguments from command line #
###################################

parser = argparse.ArgumentParser(description='Starts visioninabox.')
parser.add_argument('--headless', default=False, action='store', dest='headless', help='true to run without web interface (default: false)', type=bool)
parser.add_argument('--config_dir', default='config/', action='store', dest='config_dir', help='directory configs are stored in (default: config/)')

args = parser.parse_args()


##############################################
# Start visioninabox with provided arguments #
##############################################
vision = Vision(pathPrefix=args.config_dir, server=(not args.headless), run=True)
