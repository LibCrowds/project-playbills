#-*- coding: utf8 -*-
"""
A script for generating the project-playbills-mark projects.
"""
import re
import os
import csv
import json
import requests
import argparse
import itertools
from jinja2 import Environment, FileSystemLoader


SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(SRC_DIR, 'templates')),
    trim_blocks=False
)


def render_template(template_fn, context):
    """Render a Jinja2 template."""
    path = os.path.join(DIST_DIR, template_fn)
    tmpl = TEMPLATE_ENVIRONMENT.get_template(template_fn).render(context)
    with open(path, 'wb') as f:
        f.write(tmpl)


def generate_project_context(manifest, taskset):
    """Write and return the project.json file."""
    prefix = manifest['label'].replace('A collection of playbills from ', '')
    prefix = prefix.strip().rstrip('.').replace('"', '')
    suffix = taskset['nameSuffix']
    name = "{0}: {1}".format(prefix, suffix)
    bad_chars = r"([$#%·:,.~!¡?\"¿'=)(!&\/|]+)"
    shortname = re.sub(bad_chars, '', name.lower().strip()).replace(' ', '_')
    context = {
        "name": name,
        "short_name": shortname,
        "description": taskset['description']
    }
    path = os.path.join(DIST_DIR, 'project.json')
    with open(path, 'wb') as f:
        json.dump(context, f)
    return context


def write_tasks_csv(fieldnames, data):
    """Write the tasks.csv file."""
    path = os.path.join(DIST_DIR, 'tasks.csv')
    with open(path, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def get_task_data_from_json(json_data, taskset):
    """Return the task data generated from JSON input data."""
    task_data = taskset['tasks']
    input_data = [{'image_ark': row['info']['image_ark'],
                   'manifest_url': row['info']['manifest_url'],
                   'parent_task_id': row['task_id'],
                   'region': json.dumps(region)}
                   for row in json_data
                   for region in row['info']['regions']]

    product = list(itertools.product(task_data, input_data))
    data = [dict(row[0].items() + row[1].items()) for row in product]

    # Set default guidance
    for d in data:
        if not d['guidance']:
            d['guidance'] = ("Identify each {0} associated with the "
                             "highlighted {1}.").format(d['category'],
                                                        d['parent_category'])

    headers = set(itertools.chain(*[row.keys() for row in data]))
    return headers, data


def get_ark(f, sysno):
    """Return the ark associated with a system number."""
    reader = csv.reader(f)
    rows = [r for r in list(reader) if r[1] == str(sysno)]
    if not rows:
        raise ValueError('{0} not found'.format(sysno))
    ark = rows[0][0]
    return ark


def get_task_data_from_manifest(taskset, manifest):
    """Return the task data generated from a manifest."""
    canvases = manifest['sequences'][0]['canvases']
    images = [c['images'] for c in canvases]
    image_arks = [img[0]['resource']['service']['@id'].split('iiif/')[1]
                  for img in images]

    image_data = [{'image_ark': img_ark, 'manifest_url': manifest['@id']}
                  for img_ark in image_arks]
    task_data = taskset['tasks']
    product = list(itertools.product(task_data, image_data))
    data = [dict(row[0].items() + row[1].items()) for row in product]
    headers = set(itertools.chain(*[row.keys() for row in data]))
    return headers, data


def get_taskset(name):
    """Return the chosen taskset."""
    tasks_file = open(os.path.join(SRC_DIR, 'data', 'tasks.json'), 'rb')
    tasks_json = json.load(tasks_file)
    return tasks_json[name]


def render_templates(context):
    """Render templates."""
    here = os.path.dirname(__file__)
    src_dir = os.path.abspath(os.path.join(os.path.dirname(here), 'src'))
    render_template('template.html', context)
    render_template('tutorial.html', context)
    render_template('long_description.md', context)


def generate():
    description = '''Generate a project-playbills-mark project.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('taskset', help="A task set.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sysno', help="An Aleph system number.")
    group.add_argument('--json', help="A JSON file.")
    args = parser.parse_args()

    taskset = get_taskset(args.taskset)

    # Get the task data
    if args.json:
        json_input = json.load(open(args.json, 'rb'))
        (headers, task_data) = get_task_data_from_json(json_input, taskset)
        manifest = requests.get(task_data[0]['manifest_url']).json()
    elif args.sysno:
        csv = open(os.path.join(SRC_DIR, 'data', 'arks_and_sysnos.csv'), 'rb')
        ark = get_ark(csv, args.sysno)
        url = 'http://api.bl.uk/metadata/iiif/{0}/manifest.json'.format(ark)
        manifest = requests.get(url).json()
        (headers, task_data) = get_task_data_from_manifest(taskset, manifest)

    write_tasks_csv(headers, task_data)

    context = generate_project_context(manifest, taskset)
    render_templates(context)
    msg = '\n"{0}" created in /dist with {1} tasks\n'
    print(msg.format(context['name'], len(task_data)))


if __name__ == '__main__':
    generate()
