#-*- coding: utf8 -*-
"""
A script for generating the project-iiif-annotate project.json file.
"""
import re
import argparse
from helpers import get_task, get_csv_field, mkdist, set_config_dir, write_json


def generate_project_context(taskset, suffix):
    """Return the project context."""
    name = taskset['project']['namePrefix']
    fullname = "{0}: {1}".format(name, suffix)
    badchars = r"([$#%·:,.~!¡?\"¿'=)(!&\/|]+)"
    shortname = re.sub(badchars, '', fullname.lower().strip()).replace(' ', '_')
    context = {
        "name": fullname,
        "short_name": shortname,
        "description": taskset['project']['description']
    }
    return context


def generate(task, manifest_uri, config=None):
    """Generate the project.json file."""
    mkdist()
    set_config_dir(config)
    task = get_task(task)
    name_suffix = get_csv_field(manifest_uri, 'name')
    context = generate_project_context(task, name_suffix)
    write_json('project.json', context)
    return context


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Generate project.json.')
    PARSER.add_argument('task', help="A task listed in tasks.json.")
    PARSER.add_argument('manifest', help="IIIF manifest URI.")
    PARSER.add_argument('--config', help="Project configuration.")
    ARGS = PARSER.parse_args()
    DATA = generate(ARGS.task, ARGS.manifest, ARGS.config)
    print('\n"{0}": project.json created'.format(DATA['name']))
