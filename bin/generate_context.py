#-*- coding: utf8 -*-
"""
A script for generating the project-playbills-mark project.json file.
"""
import re
import os
import csv
import json
import argparse


SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')


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


def get_name_prefix(sysno):
    """Return name prefix associated with a system number."""
    f = open(os.path.join(SRC_DIR, 'data', 'arks_and_sysnos.csv'), 'rb')
    reader = csv.reader(f)
    rows = [r for r in list(reader) if r[1] == str(sysno)]
    if not rows:
        raise ValueError('{0} not found'.format(sysno))
    name_prefix = rows[0][2]
    return name_prefix


def get_taskset(name):
    """Return the chosen taskset."""
    tasks_file = open(os.path.join(SRC_DIR, 'data', 'tasks.json'), 'rb')
    tasks_json = json.load(tasks_file)
    return tasks_json[name]


def generate():
    description = '''Generate the project.json file.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('taskset', help="A task set.")
    parser.add_argument('sysno', help="An Aleph system number.")
    args = parser.parse_args()
    taskset = get_taskset(args.taskset)
    name_prefix = get_name_prefix(args.sysno)
    context = generate_project_context(name_prefix, taskset)
    msg = '\n"{0}": project.json created'
    print(msg.format(context['name']))


if __name__ == '__main__':
    generate()
