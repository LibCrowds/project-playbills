#-*- coding: utf8 -*-
"""
A script for generating the project-iiif-annotate tasks.
"""
import json
import argparse
import itertools
from helpers import get_task, mkdist, set_config_dir, load_json, write_json
from helpers import get_manifest

def get_share_url(manifest_url, canvas_index):
    """Return the BL Universal Viewer URL"""
    share_url_base = manifest_url.replace(
        'api.bl.uk/metadata/iiif',
        'access.bl.uk/item/viewer'
    )
    share_url_base = share_url_base.replace(
        'https://',
        'http://'
    )
    query = '#?cv={}'.format(canvas_index)
    return share_url_base.replace('/manifest.json', query)


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
    manifest_url = manifest['@id']
    canvases = manifest['sequences'][0]['canvases']
    images = [c['images'][0]['resource']['service']['@id'] for c in canvases]

    data = []
    for i, img in enumerate(images):
        row = {
            'tileSource': img + '/info.json',
            'target': canvases[i]['@id'],
            'metadata': manifest_url,
            'thumbnailUrl': img + '/full/256,/0/default.jpg',
            'shareUrl': get_share_url(manifest_url, i)
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
