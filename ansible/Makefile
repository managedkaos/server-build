TAGS = patch nginx rbase micro

playbook:
	ansible-playbook playbook.yml --verbose

list-tasks:
	ansible-playbook playbook.yml --list-tasks

$(TAGS) :
	ansible-playbook playbook.yml --tags=$@

.PHONY: playbook list-tasks $(TAGS)

