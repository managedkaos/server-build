TAGS = patch nginx rscript

playbook:
	ansible-playbook playbook.yml --verbose

list-tasks:
	ansible-playbook playbook.yml --list-tasks

$(TAGS) :
	ansible-playbook playbook.yml --tags=$@

.PHONY: all list-tasks patch solr apache2 nginx sslcert users awscli miramax_com pip check_site

