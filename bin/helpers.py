#-*- coding: utf8 -*-
"""
Helper functions for project-playbills scripts.
"""
import csv
import json
import os
import errno
import urllib2
import shutil

__all__ = ['get_task', 'get_csv_field', 'mkdist', 'get_manifest',
           'set_config_dir', 'load_json', 'copy_config_file']

DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')


def load_json(filename):
    """Return the contents of a JSON config file."""
    path = os.path.join(config_dir, filename)
    json_file = open(path, 'rb')
    return json.load(json_file)


def get_task(name):
    """Return the chosen task."""
    tasks_json = load_json('tasks.json')
    return tasks_json[name]


def get_csv_field(manifest_id, field):
    """Return the CSV metadata value adjacent to a manifest ID."""
    path = os.path.join(config_dir, 'metadata.csv')
    csv_file = open(path, 'rb')
    reader = csv.reader(csv_file)
    rows = [r for r in list(reader) if r[0] == str(manifest_id)]
    if not rows:
        raise ValueError('{0} not found in metadata.csv'.format(manifest_id))
    if field == 'name':
        return rows[0][2]
    raise ValueError('Invalid field requested from CSV file')


def mkdist():
    """Create an empty dist folder if one doesn't already exist."""
    try:
        os.makedirs(DIST_DIR)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise


def get_manifest(manifest_uri):
    """Return a manifest."""
    resp = urllib2.urlopen(manifest_uri)
    return json.load(resp)


def set_config_dir(path):
    """Return project config dir."""
    global config_dir
    if not path:
        here = os.path.dirname(__file__)
        config_dir = os.path.join(os.path.dirname(here), 'config')
        return
    config_dir = path


def write_json(filename, data):
    """Write a JSON file to the dist directory."""
    path = os.path.join(DIST_DIR, filename)
    with open(path, 'wb') as json_file:
        json.dump(data, json_file, indent=2)


def copy_config_file(src_filename, out_filename):
    """Copy a config file to the dist folder."""
    src_path = os.path.join(config_dir, src_filename)
    dist_path = os.path.join(DIST_DIR, out_filename)
    shutil.copyfile(src_path, dist_path)
