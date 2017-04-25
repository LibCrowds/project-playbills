# project-playbills-mark

Playbills marking projects for LibCrowds, designed for use with the 
[libcrowds-bs4-pybossa-theme](https://github.com/LibCrowds/libcrowds-bs4-pybossa-theme).


## Creating a new project

Choose a set of tasks from [tasks.json](tasks/tasks.json) (e.g. `"titles"`) 
and either an Aleph system number from the file 
[arks_and_sysnos.csv](tasks/arks_and_sysnos.csv), the ID of a previous marking
project or a JSON file where the info field contains the keys *aleph_sys_no*, 
*image_ark* and *regions*.

When generating tasks from an Aleph system number a new task will be created
for each permutation of image and task in the chosen set. When generating
tasks from a JSON file (which should contain the results of a previous marking 
task) a new task will be created for each result in that project, each region 
now associated with the image and each task in the chosen task set. The idea 
here being that we can chain tasks to highlight increasingly more specific 
regions in the text (e.g. all actors associated with a title). 

To generate a new project and push it to the server 
install and configure [pbs](https://github.com/Scifabric/pbs), then:

```
python generate_project.py <task set> [--sysno=<sysno> or --json=<path>]
cd gen
pbs create_project
pbs add_tasks --tasks-file=tasks.csv
pbs update-task-redundancy --redundancy 3
pbs update_project
```

Now visit the project settings page and update the category, webhook and 
thumbnail. The project is now ready to be published.


## Defining task sets

Task sets are defined in tasks.json according to the following structure:

```json
"taskset_title": {
    "nameSuffix": "Appended to the title of the catalogue record to create the project title",
    "description": "A one line description of the project",
    "tasks": [
        {
            "category": "some_category",
            "objective": "The objective of the task",
            "guidance": "Additional guidance"
        }
    ]
}
```

Note that if `guidance` is set to `null` and the task set is being generated from
the results of a previous makring project then the guidance will be generated automatically
in the form "Identify each <category> associated with the highlighted <parent task category>.".
