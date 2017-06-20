# project-playbills-mark

Playbills marking projects for LibCrowds.

## Creating a new project

Choose a set of tasks from [tasks.json](input/tasks.json) (e.g. `"titles"`) 
and either an Aleph system number from the file 
[arks_and_sysnos.csv](input/arks_and_sysnos.csv) or a JSON file containing
the results data of a previous marking project.

When generating tasks from an Aleph system number a task will be created
for each permutation of image and task in the chosen set. When generating
tasks from a JSON results file a task will be created for each result, each 
region now associated with the result and each task in the chosen task set. 
The idea being that we can chain tasks to highlight increasingly more specific 
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

Now from the project settings page on the server:

- Update the category
- Set the webhook to http://analyse.libcrowds.com/playbills
- Set a project thumbnail
- Publish the project

The project is now ready to be published.

## Defining task sets

Task sets are defined in [input/tasks.json](input/tasks.json) with the 
following structure:

```json
"name": {
  "nameSuffix": "Appended to the catalogue title to create the project title",
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

Note that if `guidance` is set to `null` and the task set is being generated 
from the results of a previous marking project then the guidance will be 
generated automatically in the form "Identify each <category> associated with 
the highlighted <parent task category>.".
