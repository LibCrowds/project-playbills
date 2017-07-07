#-*- coding: utf8 -*-
"""
A script for generating the project-playbills-mark project.json file.
"""
import re
import os
import json
import argparse
from helpers import get_taskset, get_csv_field, mkdist
from helpers import DIST_DIR


def generate_project_context(name_prefix, taskset):
    """Write and return the project.json file."""
    suffix = taskset['nameSuffix']
    name = "{0}: {1}".format(name_prefix, suffix)
    bad_chars = r"([$#%·:,.~!¡?\"¿'=)(!&\/|]+)"
    shortname = re.sub(bad_chars, '', name.lower().strip()).replace(' ', '_')
    context = {
        "name": name,
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
    parser.add_argument('taskset', help="A task set.")
    parser.add_argument('sysno', help="An Aleph system number.")
    args = parser.parse_args()
    
    mkdist()
    taskset = get_taskset(args.taskset)
    name_prefix = get_csv_field(args.sysno, 'name')
    context = generate_project_context(name_prefix, taskset)
    msg = '\n"{0}": project.json created'
    print(msg.format(context['name']))


if __name__ == '__main__':
    generate()
