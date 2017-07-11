#-*- coding: utf8 -*-
"""
A script for generating the project-iiif-mark project.json file.
"""
import re
import os
import json
import argparse
from helpers import get_task, get_csv_field, mkdist, set_config_dir
from helpers import DIST_DIR


def write_project_context(context):
    """Return the project.json file."""
    path = os.path.join(DIST_DIR, 'project.json')
    with open(path, 'wb') as f:
        json.dump(context, f, indent=2)


def generate_project_context(taskset, suffix):
    """Return the project context."""
    name = taskset['name']
    fullname = "{0}: {1}".format(name, suffix)
    badchars = r"([$#%·:,.~!¡?\"¿'=)(!&\/|]+)"
    shortname = re.sub(badchars, '', fullname.lower().strip()).replace(' ', '_')
    context = {
        "name": fullname,
        "short_name": shortname,
        "description": taskset['description']
    }
    return context


def generate(task, manifestid, config=None):
    """Generate the project.json file."""
    mkdist()
    set_config_dir(config)
    task = get_task(task)
    name_suffix = get_csv_field(manifestid, 'name')
    context = generate_project_context(task, name_suffix)
    write_project_context(context)
    return context


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Generate project.json.')
    PARSER.add_argument('task', help="A task listed in tasks.json.")
    PARSER.add_argument('manifestid', help="IIIF manifest ID.")
    PARSER.add_argument('--config', help="Project configuration.")
    ARGS = PARSER.parse_args()
    DATA = generate(ARGS.task, ARGS.manifestid, ARGS.config)
    print('\n"{0}": project.json created'.format(DATA['name']))
