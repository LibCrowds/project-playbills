#-*- coding: utf8 -*-
"""
A script for generating the tasks for a project-playbills-mark project.
"""
import re
import os
import csv
import json
import urllib2
import argparse
import itertools
from helpers import get_taskset, get_csv_field, mkdist
from helpers import DIST_DIR


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


def generate():
    description = '''Generate the tasks for a project-playbills-mark project.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('taskset', help="A task set.")
    parser.add_argument('sysno', help="An Aleph system number.")
    parser.add_argument('--results', help="A JSON file.")
    args = parser.parse_args()

    mkdist()
    taskset = get_taskset(args.taskset)

    ark = get_csv_field(args.sysno, 'ark')
    url = 'http://api.bl.uk/metadata/iiif/{0}/manifest.json'.format(ark)
    print url
    manifest = json.load(urllib2.urlopen(url))

    # Generate the task data
    if args.results:
        results_json = json.load(open(args.results, 'rb'))
        (headers, task_data) = get_task_data_from_json(results_json, taskset)
    else:
        (headers, task_data) = get_task_data_from_manifest(taskset, manifest)
    write_tasks_csv(headers, task_data)

    msg = '\n{0} tasks created'.format(len(task_data))
    print(msg)


if __name__ == '__main__':
    generate()
