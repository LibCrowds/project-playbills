#-*- coding: utf8 -*-
"""
A script for generating the project-iiif-annotate tasks.
"""
import json
import argparse
import itertools
from helpers import get_task, mkdist, set_config_dir, load_json, write_json
from helpers import get_manifest


def get_task_data_from_json(json_data, taskset):
    """Return the task data generated from JSON input data."""
    task_data = taskset['tasks']
    input_data = [{'img_info_uri': row['info']['img_info_uri'],
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


def get_task_data_from_manifest(category, manifest):
    """Return the task data generated from a manifest."""
    task = get_task(category)
    canvases = manifest['sequences'][0]['canvases']
    images = [c['images'] for c in canvases]
    img_uris = [img[0]['resource']['service']['@id'] + '/info.json'
                for img in images]
    data = []
    for uri in img_uris:
        row = {
            'imgInfoUri': uri,
            'manifestUri' manifest['@id']
        }
        row.update(task['task'])
        data.append(row)
    return data


def generate(category, manifest_id, config=None, results=None):
    """Generate and return the tasks file."""
    mkdist()
    set_config_dir(config)
    if results:
        results_json = json.load(open(results, 'rb'))
        task_data = get_task_data_from_json(results_json, category)
    else:
        manifest = get_manifest(manifest_id)
        task_data = get_task_data_from_manifest(category, manifest)
    write_json('tasks.json', task_data)
    return task_data


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Generate tasks")
    PARSER.add_argument('category', help="A task category in tasks.json.")
    PARSER.add_argument('manifestid', help="IIIF manifest ID.")
    PARSER.add_argument('--config', help="Project configuration.")
    PARSER.add_argument('--results', help="JSON results file.")
    ARGS = PARSER.parse_args()
    DATA = generate(ARGS.category, ARGS.manifestid, ARGS.config, ARGS.results)
    print'\n{0} tasks created'.format(len(DATA))
