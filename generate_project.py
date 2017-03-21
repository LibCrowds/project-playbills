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
from BeautifulSoup import BeautifulSoup


def verify_arks(data):
    """Identify any arks that don't point to images via the BL IIIF api."""
    for row in data:
        ark = row['image_ark']
        url = 'http://api.bl.uk/image/iiif/{}/info.json'.format(ark)
        r = requests.get(url)
        info = r.json()
        if not info.get('tiles'):
            raise ValueError('Bad Ark: {}'.format(ark))


def update_shortname(old_project_json, new_project_json):
    """Update the short name in template and results files."""
    here = os.path.dirname(__file__)
    old = old_project_json['short_name']
    new = new_project_json['short_name']
    def replace(fn):
        path_in = os.path.join(here, fn)
        path_out = os.path.join(here, 'gen', fn)
        with open(path_in, 'rb') as f:
            data_in = f.read()
        data_out = data_in.replace(old, new)
        with open(path_out, 'wb') as f:
            f.write(data_out)
    replace('results.html')
    replace('template.html')


def copy_project_files():
    """Copy template, tutorial, long_description and result files to gen."""
    here = os.path.dirname(__file__)
    def copy(fn):
        shutil.copyfile(os.path.join(here, fn), os.path.join(here, 'gen', fn))
    copy('long_description.md')
    copy('template.html')
    copy('tutorial.html')
    copy('results.html')


def write_project_json(rec_title, taskset):
    """Write the project.json file."""
    prefix = 'A collection of playbills from '
    title = rec_title.replace(prefix, '').strip().rstrip('.').replace('"', '')
    name_suffix = taskset['nameSuffix']
    name = "{0}: {1}".format(title, name_suffix)
    invalidchars = r"([$#%·:,.~!¡?\"¿'=)(!&\/|]+)"
    shortname = re.sub(invalidchars, '', name.lower().strip()).replace(' ', '_')
    project = {
        "name": name,
        "short_name": shortname,
        "description": taskset['description']
    }
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'gen', 'project.json')
    with open(path, 'wb') as f:
        json.dump(project, f)
    return project


def write_tasks_csv(fieldnames, data):
    """Write the tasks.csv file."""
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'gen', 'tasks.csv')
    with open(path, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def get_json_data(json_data, taskset):
    """Return the task data generated from JSON input data."""
    tasks = taskset['tasks']

    # Get permutations of each image and associated region
    input_data = [{'image_ark': row['info']['image_ark'],
                   'aleph_sys_no': row['info']['aleph_sys_no'],
                   'parent_task_id': row['task_id'],
                   'region': json.dumps(region)}
                   for row in json_data 
                   for region in row['info']['regions']]
    
    product = list(itertools.product(tasks, input_data))
    data = [dict(row[0].items() + row[1].items()) for row in product]
    headers = set(itertools.chain(*[row.keys() for row in data]))
    return headers, data


def get_ark_aleph_data(csv_path, taskset, aleph_sysno):
    """Return the task data generated from the input csv file."""
    tasks = taskset['tasks']
    with open(csv_path, 'rb') as f:
        reader = csv.reader(f)
        l = list(reader)
        headers = l[0] + sorted(tasks[0])
        data = [{'image_ark': r[0], 'aleph_sys_no': r[1]} 
                for r in l[1:] if r[1] == aleph_sysno]
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

def get_record_title(aleph_sysno):
    """Attempt to retreive the title of the record from ALEPH."""
    base_url = "http://primocat.bl.uk/F/"
    url = "{0}?func=direct&local_base=PRIMO&doc_number={1}".format(base_url,
                                                                   aleph_sysno)
    resp = requests.get(url)
    html = BeautifulSoup(resp.text)
    rows = data = [td.findChildren(text=True) for td in html.findAll("td")]
    for i, td in enumerate(rows):
        if td and 'Title &nbsp;' in td[0]:
            return rows[i + 1][0]
    raise ValueError('No title for that system number could not be found')


def generate():
    description = '''Generate a project-playbills-mark project.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('taskset', help="A task set.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sysno', help="An Aleph system number.")
    group.add_argument('--json', help="A JSON file.")
    args = parser.parse_args()

    here = os.path.dirname(__file__)
    tasks_path = os.path.join(here, 'tasks.json')
    tasks_json = json.load(open(tasks_path, 'rb'))
    taskset = tasks_json[args.taskset]
    project_json_path = os.path.join(here, 'project.json')
    old_project_json = json.load(open(project_json_path, 'rb'))

    # Get the task data
    if args.json:
        json_input = json.load(open(args.json, 'rb'))
        (headers, data) = get_json_data(json_input, taskset)
        sysno = data[1]['aleph_sys_no']
    elif args.sysno:
        arks_path = os.path.join(here, 'input', 'arks_and_aleph_sys_nos.csv')
        sysno = args.sysno
        (headers, data) = get_ark_aleph_data(arks_path, taskset, args.sysno)

    verify_arks(data)
    make_gen_dir()
    write_tasks_csv(headers, data)
    title = get_record_title(sysno)
    new_project_json = write_project_json(title, taskset)
    copy_project_files()
    update_shortname(old_project_json, new_project_json)
    msg = '\n"{0}" created with {1} tasks'
    print(msg.format(new_project_json['name'], len(data)))

if __name__ == '__main__':
    generate()
