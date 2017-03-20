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
from BeautifulSoup import BeautifulSoup


def verify_arks(data):
    """Identify any arks that don't point to images via the BL IIIF api."""
    for row in data[1:]:
        ark = row[0]
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
        print old, new
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

    
def write_tasks_csv(data):
    """Write the tasks.csv file."""
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'gen', 'tasks.csv')
    with open(path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def get_ark_aleph_data(csv_path, taskset, aleph_sysno):
    """Return the task data generated from the input csv file."""
    tasks = taskset['tasks']
    with open(csv_path, 'rb') as f:
        reader = csv.reader(f)
        l = list(reader)
        headers = l[0] + sorted(tasks[0])
        data = {}
        for r in l[1:]:
            sys_no = r[1]
            row = [r + [t[k] for k in sorted(t)] for t in tasks]
            data[sys_no] = data.get(sys_no, []) + row
        return [headers] + data[aleph_sysno]

        
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
    group.add_argument('--id', help="A project ID.")
    args = parser.parse_args()
    
    here = os.path.dirname(__file__)
    tasks_path = os.path.join(here, 'tasks.json')
    arks_path = os.path.join(here, 'input', 'ark_and_aleph_system_numbers.csv')
    tasks_json = json.load(open(tasks_path, 'rb'))
    taskset = tasks_json[args.taskset]
    record_title = get_record_title(args.sysno)
    default_project_json_path = os.path.join(here, 'project.json')
    default_project_json = json.load(open(default_project_json_path, 'rb'))

    if args.id:
        pass
    elif args.sysno:
        data = get_ark_aleph_data(arks_path, taskset, args.sysno)
    
    verify_arks(data)
    make_gen_dir()
    write_tasks_csv(data)
    project_json = write_project_json(record_title, taskset)
    copy_project_files()
    update_shortname(default_project_json, project_json)

    
if __name__ == '__main__':
    generate()
    