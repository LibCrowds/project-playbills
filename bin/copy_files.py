#-*- coding: utf8 -*-
"""
A script for copying otherwise unprocessed config files to the dist folder.
"""
import argparse
from helpers import set_config_dir, copy_config_file


def copy(config=None):
    """Copy files to the dist folder."""
    set_config_dir(config)
    copy_config_file('long_description.md')
    copy_config_file('pybossa.json')


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Copy config files.')
    PARSER.add_argument('--config', help="Project configuration.")
    ARGS = PARSER.parse_args()
    copy(ARGS.config)
