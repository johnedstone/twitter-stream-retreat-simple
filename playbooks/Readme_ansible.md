### Ansible Notes:
This Ansible playbookis under development 

#### Ansible sequence
```
ansible-playbook --check --diff --flush-cache --tags prep-work -i inventory.ini playbook.yaml
ansible-playbook --diff --flush-cache --tags prep-work -i inventory.ini playbook.yaml
```
Then reboot


ansible-playbook --check --flush-cache --diff -i inventory.ini playbook.yaml 

ansible-playbook --flush-cache --diff -i inventory.ini playbook.yaml

ansible-playbook --flush-cache --tags virtualenv --diff -i inventory.ini playbook.yaml
```

### First time running Ansible
Since some the `install_app` playbook depends on a directory created in the
earlier playbooks, then the first time run this sequence

```
ansible-playbook --check --tags prepwork,virtualenv --flush-cache --diff -i inventory.ini playbook.yaml
ansible-playbook --tags prepwork,virtualenv --flush-cache --diff -i inventory.ini playbook.yaml

ansible-playbook --check --flush-cache --diff -i inventory.ini playbook.yaml
ansible-playbook --flush-cache --diff -i inventory.ini playbook.yaml
```

