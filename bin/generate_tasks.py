#-*- coding: utf8 -*-
"""
A script for generating the project-playbills tasks.
"""
import json
import argparse
from helpers import get_task, mkdist, set_config_dir, write_json
from helpers import get_manifest, load_markdown


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


def enhance_task_data_from_results(task_data, results):
    """Return the task data generated from JSON input data."""
    # Index task_data by target
    indexed_task_data = {row['target']: row for row in task_data}

    enhanced_task_data = []
    for row in results:
        info = row['info']

        if not info:
            raise ValueError('The info field for a result is empty')
        annotations = info['annotations']

        for anno in annotations:
            if anno['motivation'] == 'tagging':
                source = anno['target']['source']
                selector = anno['target']['selector']['value']
                rect = selector.split('=')[1].split(',')
                data = indexed_task_data[source].copy()
                data['highlights'] = [
                    {
                        'x': float(rect[0]),
                        'y': float(rect[1]),
                        'width': float(rect[2]),
                        'height': float(rect[3])
                    }
                ]
                data['bounds'] = {
                    'x': float(rect[0]) + data['bounds']['x'],
                    'y': float(rect[1]) + data['bounds']['y'],
                    'width': float(rect[2]) + data['bounds']['width'],
                    'height': float(rect[3]) + data['bounds']['height']
                }
                data['parent_task_id'] = row['task_id']
                enhanced_task_data.append(data)
            elif anno['motivation'] != 'commenting':
                raise ValueError('Unknown motivation')

    # Sort
    return sorted(enhanced_task_data,
                  key=lambda x: (
                      x['target'],
                      x['highlights'][0]['y'],
                      x['highlights'][0]['x']
                  ))


def get_task_data_from_manifest(task, manifest):
    """Return the task data generated from a manifest."""
    manifest_url = manifest['@id']
    canvases = manifest['sequences'][0]['canvases']
    images = [c['images'][0]['resource']['service']['@id'] for c in canvases]

    data = []
    for i, img in enumerate(images):
        row = {
            'tileSource': img + '/info.json',
            'target': canvases[i]['@id'],
            'info': manifest_url,
            'thumbnailUrl': img + '/full/256,/0/default.jpg',
            'shareUrl': get_share_url(manifest_url, i)
        }
        row.update(task['task'])
        data.append(row)
    return data


def generate(category, manifest_id, config=None, results=None, skip=None):
    """Generate and return the tasks file."""
    mkdist()
    set_config_dir(config)

    task = get_task(category)
    manifest = get_manifest(manifest_id)
    task_data = get_task_data_from_manifest(task, manifest)
    help_path = task['project'].get('help')

    if help_path:
      _help = load_markdown(help_path)
      for row in task_data:
        row['help'] = _help

    if task['project']['parent'] and not results:
        err_msg = '{0} projects must be built from the results of a {1} project'
        err_msg = err_msg.format(category, task['project']['parent'])
        raise ValueError(err_msg)

    elif results:
        results_json = json.load(open(results, 'rb'))
        task_data = enhance_task_data_from_results(task_data, results_json)

    if skip:
        task_data = task_data[int(skip):]

    write_json('raw_tasks.json', task_data)

    # Fix for "info" field also being used for metadata in task opts
    task_data = [{'info': task} for task in task_data]
    write_json('tasks.json', task_data)
    return task_data


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Generate tasks")
    PARSER.add_argument('category', help="A task category in tasks.json.")
    PARSER.add_argument('manifestid', help="IIIF manifest ID.")
    PARSER.add_argument('--config', help="Project configuration.")
    PARSER.add_argument('--results', help="JSON results file.")
    PARSER.add_argument('--skip', help="Skip the first n tasks.")
    ARGS = PARSER.parse_args()
    DATA = generate(ARGS.category, ARGS.manifestid, ARGS.config, ARGS.results,
                    ARGS.skip)
    print'\n{0} tasks created'.format(len(DATA))
