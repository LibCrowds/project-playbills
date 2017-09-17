#-*- coding: utf8 -*-
"""
A script for generating the project-playbills help.json file.
"""
import re
import argparse
from helpers import get_task, set_config_dir, copy_config_file


def generate(task, config=None):
    """Generate the tutorial.md file."""
    set_config_dir(config)
    task = get_task(task)
    copy_config_file(task['tutorial'], 'tutorial.md')


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Generate tutorial.md.')
    PARSER.add_argument('task', help="A task listed in tasks.json.")
    PARSER.add_argument('--config', help="Project configuration.")
    ARGS = PARSER.parse_args()
    generate(ARGS.task, ARGS.config)
    print('tutorial.md created')
