"""
A script for generating the tasks for project-playbills-mark.
"""
import os
import csv
import json
import argparse
import itertools


def write_csv(path, data, headers):
    """Write the data to a csv file."""
    with open(path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)


def read_csv(path, questions):
    """Return the question data generated for the csv and json files."""
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        l = list(reader)
        headers = l[0] + sorted(questions[0])
        data = {}
        for r in l[1:]:
            sys_no = r[1]
            row = [r + [q[k] for k in sorted(q)] for q in questions]
            data[sys_no] = data.get(sys_no, []) + row
        return data, headers


if __name__ == '__main__':
    description = '''Generate tasks for project-playbills-mark.
    
    By default it loads ark_and_aleph_system_numbers.csv, adds a row for each category defined in categories.json, 
    then generates a csv file containing the tasks for the given Aleph System number.
    '''
    here = os.path.dirname(__file__)
    default_csv = os.path.join(here, 'ark_and_aleph_system_numbers.csv')
    default_json = os.path.join(here, 'categories.json')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('sysno', help="The Aleph system number.")
    parser.add_argument('--arks', default=default_csv, help="The CSV input file.")
    parser.add_argument('--categories', default=default_json, help="The JSON input file.")
    args = parser.parse_args()
    categories = json.load(open(args.categories, 'rb'))
    data, headers = read_csv(args.arks, categories)
    out_path = os.path.join(os.path.dirname(here), 'tasks.csv')
    write_csv(out_path, data[args.sysno], headers)
