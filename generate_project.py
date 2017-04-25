#-*- coding: utf8 -*-
"""
A script for generating the project-playbills-mark projects.
"""
import re
import os
import csv
import json
import errno
import requests
import argparse
import shutil
import itertools
from jinja2 import Environment, FileSystemLoader


TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.dirname(__file__)),
    trim_blocks=False
)


def render_template(template_filename, context):
    """Render a Jinja2 template."""
    path = os.path.join(os.path.dirname(__file__), 'gen', template_filename)
    tmpl = TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
    with open(path, 'wb') as f:
        f.write(tmpl)


def generate_project_context(manifest, taskset):
    """Write and return the project.json file."""
    prefix = manifest['label'].replace('A collection of playbills from ', '')
    prefix = prefix.strip().rstrip('.').replace('"', '')
    suffix = taskset['nameSuffix']
    name = "{0}: {1}".format(prefix, suffix)
    invalidchars = r"([$#%·:,.~!¡?\"¿'=)(!&\/|]+)"
    shortname = re.sub(invalidchars, '', name.lower().strip()).replace(' ', '_')
    context = {
        "name": name,
        "short_name": shortname,
        "description": taskset['description']
    }
    here = os.path.dirname(__file__)
    path = os.path.join(os.path.dirname(__file__), 'gen', 'project.json')
    with open(path, 'wb') as f:
        json.dump(context, f)
    return context


def write_tasks_csv(fieldnames, data):
    """Write the tasks.csv file."""
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'gen', 'tasks.csv')
    with open(path, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def get_task_data_from_json(json_data, taskset):
    """Return the task data generated from JSON input data."""
    task_data = taskset['tasks']
    input_data = [{'image_ark': row['info']['image_ark'],
                   'manifest_id': row['info']['manifest_id'],
                   'parent_category': row['info']['category'],
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

    
def get_ark(csv_path, sysno):
    """Return the ark associated with a system number."""
    with open(csv_path, 'rb') as f:
        reader = csv.reader(f)
        rows = [r for r in list(reader) if r[1] == str(sysno)]
        if not rows:
            raise ValueError('{0} not found in {1}'.format(sysno, csv_path))
        ark = rows[0][0]
        return ark


def get_task_data_from_manifest(taskset, manifest):
    """Return the task data generated from a manifest."""
    canvases = manifest['sequences'][0]['canvases']
    images = [c['images'] for c in canvases]
    image_arks = [img[0]['resource']['service']['@id'].split('iiif/')[1] 
                  for img in images]
    
    image_data = [{'image_ark': img_ark, 'manifest_id': manifest['@id']} 
                  for img_ark in image_arks]
    task_data = taskset['tasks']
    product = list(itertools.product(task_data, image_data))
    data = [dict(row[0].items() + row[1].items()) for row in product]
    headers = set(itertools.chain(*[row.keys() for row in data]))
    return headers, data
    
    
def make_gen_dir():
    """Ensure that an empty gen directory exists."""
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'gen')
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno == errno.EEXIST:
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            raise


def generate():
    description = '''Generate a project-playbills-mark project.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('taskset', help="A task set.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sysno', help="An Aleph system number.")
    group.add_argument('--json', help="A JSON file.")
    args = parser.parse_args()

    here = os.path.dirname(__file__)
    tasks_json = json.load(open(os.path.join(here, 'tasks.json'), 'rb'))
    taskset = tasks_json[args.taskset]

    # Get the task data
    if args.json:
        json_input = json.load(open(args.json, 'rb'))
        (headers, task_data) = get_task_data_from_json(json_input, taskset)
        manifest = requests.get(task_data[0]['manifest_id']).json()
    elif args.sysno:
        csv_path = os.path.join(here, 'input', 'arks_and_sysnos.csv')
        ark = get_ark(csv_path, args.sysno)
        url = 'http://api.bl.uk/metadata/iiif/{0}'.format(ark)
        manifest = requests.get(url).json()
        (headers, task_data) = get_task_data_from_manifest(taskset, manifest)

    make_gen_dir()
    write_tasks_csv(headers, task_data)
    context = generate_project_context(manifest, taskset)
    render_template('tutorial.html', context)
    render_template('template.html', context)
    render_template('results.html', context)
    render_template('long_description.md', context)
    msg = '\n"{0}" created with {1} tasks'
    print(msg.format(context['name'], len(task_data)))

    
if __name__ == '__main__':
    generate()
