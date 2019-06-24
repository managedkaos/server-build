TAGS = patch nginx rbase micro apache2

playbook:
	ansible-playbook playbook.yml --verbose

list-tasks:
	ansible-playbook playbook.yml --list-tasks

$(TAGS) :
	ansible-playbook playbook.yml --tags=$@ --verbose

.PHONY: playbook list-tasks $(TAGS)

