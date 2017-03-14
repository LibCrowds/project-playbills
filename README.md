# project-playbills-mark

Playbills marking project for LibCrowds, initially designed for use with the 
[libcrowds-bs4-pybossa-theme](https://github.com/LibCrowds/libcrowds-bs4-pybossa-theme).


## Creating a new project

Install and configure [pbs](https://github.com/Scifabric/pbs).

Generate the tasks:

```
python generate_tasks.py <Aleph system number>
```

Create the project:
```
python create_project.py <endpoint> <api_key>
```

The first script generates the tasks for a given Aleph system number. The second creates a new project using a name 
derived from the title of the catalogue record, adds the tasks and sets the task redundancy. The project can now be
published from the project settings page.