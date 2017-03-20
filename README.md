# project-playbills-mark

Playbills projects for LibCrowds, designed for use with the 
[libcrowds-bs4-pybossa-theme](https://github.com/LibCrowds/libcrowds-bs4-pybossa-theme).


## Creating a new project

Install and configure [pbs](https://github.com/Scifabric/pbs).

Choose a set of tasks from [tasks.json](tasks/tasks.json) (e.g. `"mark_performances"`) 
and choose an input file. The marking tasks expect a CSV file containing the 
columns *image_ark* and *aleph_sys_no*, and an optional column *regions* The 
transcription tasks expect all of these columns.

In reality, the `"mark_performances"` tasks will be generated from 
[ark_and_aleph_system_numbers.csv](tasks/ark_and_aleph_system_numbers.csv) and
further task sets will be generated from the results files produced by a project
with a task set of the type identified in `"parent"`.

The [generate_tasks.py](generate_tasks.py) script is provided to handle the 
multiple versions of each type of project that will be created, according to the
data specified in [tasks.json](tasks/tasks.json). 

So, to generate a new project and push it to the server:

```
python generate_project.py <task set> <input csv>
cd /gen
pbs create_project
pbs update-task-redundancy --redundancy 3
pbs update_project
```

The project can now be published from the project settings page.