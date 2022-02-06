### Example ansible commands
```
ansible-playbook --version
ansible-playbook 2.9.6
  config file = /opt/apps/twitter-stream-retreat-simple/playbooks/ansible.cfg
  configured module search path = ['/home/ubuntu/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible-playbook
  python version = 3.8.10 (default, Nov 26 2021, 20:14:08) [GCC 9.3.0]

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

