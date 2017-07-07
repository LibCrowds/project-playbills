#-*- coding: utf8 -*-
"""
A script for generating the project-playbills-mark project.json file.
"""
import re
import os
import json
import argparse
from helpers import get_task, get_csv_field, mkdist, get_config_dir
from helpers import DIST_DIR


def generate_project_context(taskset, suffix):
    """Write and return the project.json file."""
    name = taskset['name']
    fullname = "{0}: {1}".format(name, suffix)
    badchars = r"([$#%·:,.~!¡?\"¿'=)(!&\/|]+)"
    shortname = re.sub(badchars, '', fullname.lower().strip()).replace(' ', '_')
    context = {
        "name": fullname,
        "short_name": shortname,
        "description": taskset['description']
    }
    path = os.path.join(DIST_DIR, 'project.json')
    with open(path, 'wb') as f:
        json.dump(context, f, indent=2)
    return context


def generate():
    description = '''Generate the project.json file.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('task', help="A task listed in tasks.json.")
    parser.add_argument('manifestid', help="IIIF manifest ID.")
    parser.add_argument('--config', help="Project configuration.")
    args = parser.parse_args()

    mkdist()
    config_dir = get_config_dir(args.config)
    task = get_task(config_dir, args.task)
    name_suffix = get_csv_field(config_dir, args.manifestid, 'name')
    context = generate_project_context(task, name_suffix)
    msg = '\n"{0}": project.json created'
    print(msg.format(context['name']))


if __name__ == '__main__':
    generate()
