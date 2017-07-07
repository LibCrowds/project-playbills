#-*- coding: utf8 -*-
"""
A script for generating the tasks for a project-playbills-mark project.
"""
import os
import json
import urllib2
import argparse
import itertools
from helpers import get_task, get_csv_field, mkdist, get_config_dir, load_json
from helpers import get_manifest
from helpers import DIST_DIR


def write_tasks_json(config_dir, task_data, manifest_id):
    """Write the tasks.json file."""
    path = os.path.join(DIST_DIR, 'tasks.json')

    # Add iiif config for all tasks
    iiif_json = load_json(config_dir, 'iiif.json')
    print iiif_json
    for obj in task_data:
      obj.update(iiif_json)

    with open(path, 'wb') as f:
        json.dump(task_data, f, indent=2)


def get_task_data_from_json(json_data, taskset):
    """Return the task data generated from JSON input data."""
    task_data = taskset['tasks']
    input_data = [{'image_id': row['info']['image_id'],
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
    return data


def get_task_data_from_manifest(config_dir, category, manifest):
    """Return the task data generated from a manifest."""
    task = get_task(config_dir, category)
    canvases = manifest['sequences'][0]['canvases']
    images = [c['images'] for c in canvases]
    image_arks = [img[0]['resource']['service']['@id'].split('iiif/')[1]
                  for img in images]
    data = [{
      'image_id': img_ark,
      'category': category,
      'objective': task['objective'],
      'guidance': task['guidance']
    } for img_ark in image_arks]
    return data


def generate():
    description = '''Generate the tasks for a project-playbills-mark project.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('category', help="A task category in tasks.json.")
    parser.add_argument('manifestid', help="IIIF manifest ID.")
    parser.add_argument('--config', help="Project configuration.")
    parser.add_argument('--results', help="JSON results file.")
    args = parser.parse_args()

    mkdist()
    config_dir = get_config_dir(args.config)

    # Generate the task data
    if args.results:
        results_json = json.load(open(args.results, 'rb'))
        task_data = get_task_data_from_json(results_json, category)
    else:
        manifest = get_manifest(config_dir, args.manifestid)
        task_data = get_task_data_from_manifest(config_dir, args.category, manifest)
    write_tasks_json(config_dir, task_data, args.manifestid)

    msg = '\n{0} tasks created'.format(len(task_data))
    print(msg)


if __name__ == '__main__':
    generate()
