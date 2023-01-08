### Ansible Notes:
This Ansible playbookis under development 

#### Ansible sequence
```
ansible-playbook --check --diff --flush-cache --tags prep-work -i inventory.ini playbook.yaml
ansible-playbook --diff --flush-cache --tags prep-work -i inventory.ini playbook.yaml
```

Then reboot

```
ansible-playbook --check --diff --flush-cache --tags virtualenv -i inventory.ini playbook.yaml
ansible-playbook --diff --flush-cache --tags virtualenv -i inventory.ini playbook.yaml

ansible-playbook --check --diff --flush-cache --tags install-app -i inventory.ini playbook.yaml
ansible-playbook --diff --flush-cache --tags install-app -i inventory.ini playbook.yaml
```

And then finally:
```
ansible-playbook --check --diff --flush-cache -i inventory.ini playbook.yaml
ansible-playbook --diff --flush-cache -i inventory.ini playbook.yaml
```
