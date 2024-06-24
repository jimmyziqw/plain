import yaml
import subprocess

with open('tasks.yml', 'r') as file:
    tasks = yaml.safe_load(file)

for task in tasks['tasks']:
    print(f"Running {task['name']}...")
    for cmd in task['cmds']:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    print(f"{task['name']} done.")
