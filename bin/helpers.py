#-*- coding: utf8 -*-
"""
Helper functions for project-iiif-mark scripts.
"""
import os
import csv
import json
import os
import errno
import urllib2

__all__ = ['SRC_DIR', 'DIST_DIR', 'get_task', 'get_csv_field', 'mkdist',
           'get_manifest', 'get_config_dir', 'load_josn']

DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')


def load_json(config_dir, fn):
    """Return the contents of a JSON config file."""
    path = os.path.join(config_dir, fn)
    f = open(path, 'rb')
    return json.load(f)


def get_task(config_dir, name):
    """Return the chosen task."""
    tasks_json = load_json(config_dir, 'tasks.json')
    return tasks_json[name]


def get_csv_field(config_dir, manifest_id, field):
    """Return the CSV metadata value adjacent to a manifest ID."""
    path = os.path.join(config_dir, 'metadata.csv')
    f = open(path, 'rb')
    reader = csv.reader(f)
    rows = [r for r in list(reader) if r[0] == str(manifest_id)]
    if not rows:
        raise ValueError('{0} not found in metadata.csv'.format(manifest_id))
    if field == 'name':
      return rows[0][1]
    raise ValueError('Invalid field requested from CSV file')


def mkdist():
    """Create an empty dist folder if one doesn't already exist."""
    try:
      os.makedirs(DIST_DIR)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_manifest(config_dir, manifest_id):
    """Return a manifest."""
    iiif_json = load_json(config_dir, 'iiif.json')
    base = '{0}://{1}/{2}/{3}/manifest.json'
    url = base.format(iiif_json['scheme'], iiif_json['server'],
                      iiif_json['presentation_api_prefix'], manifest_id)
    resp = urllib2.urlopen(url)
    manifest = json.load(resp)
    return manifest


def get_config_dir(path):
    """Return project config dir."""
    if not path:
      here = os.path.dirname(__file__)
      return os.path.join(os.path.dirname(here), 'config')
    return path
