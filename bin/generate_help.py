#-*- coding: utf8 -*-
"""
A script for generating the project-playbills help.json file.
"""
import re
import argparse
from helpers import get_task, mkdist, set_config_dir, write_json


def generate(task, config=None):
    """Generate the project.json file."""
    mkdist()
    set_config_dir(config)
    task = get_task(task)
    _help = task['help']
    write_json('help.json', _help)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Generate help.json.')
    PARSER.add_argument('task', help="A task listed in tasks.json.")
    PARSER.add_argument('--config', help="Project configuration.")
    ARGS = PARSER.parse_args()
    generate(ARGS.task, ARGS.config)
    print('help.json created')
