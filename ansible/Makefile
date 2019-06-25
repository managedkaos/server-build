TAGS = patch nginx rbase micro apache2 libraries packages upload

playbook:
	ansible-playbook playbook.yml --verbose

list-tasks:
	ansible-playbook playbook.yml --list-tasks

ssh:
	ssh -i ~/.ssh/cloudformation.pem ubuntu@ec2-3-82-123-159.compute-1.amazonaws.com

$(TAGS) :
	ansible-playbook playbook.yml --tags=$@ --verbose

.PHONY: playbook list-tasks ssh $(TAGS)
