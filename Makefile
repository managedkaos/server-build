AWS=$(VIRTUAL_ENV)/bin/aws
STACKNAME=server-stack
KEYNAME=$(STACKNAME)
SSHUSER=ubuntu

$(STACKNAME).yml: $(STACKNAME).py
	python $< | tee $@

lint: $(STACKNAME).py
	pylint --rcfile=.pylint_config $<

clean:
	@rm $(STACKNAME).yml || echo "All clean! :D"

stack: $(STACKNAME).yml
	@$(AWS) cloudformation create-stack \
		--stack-name $(STACKNAME) \
		--template-body file://$(STACKNAME).yml \
		--tags Key=Name,Value=$(STACKNAME) \
		--parameters ParameterKey=KeyName,ParameterValue=$(KEYNAME)
	 $(AWS) cloudformation wait stack-create-complete \
		 --stack-name $(STACKNAME)
	 $(AWS) cloudformation describe-stacks \
		 --stack-name $(STACKNAME) --query="Stacks[].Outputs" --output=table

describe-stack:
	 $(AWS) cloudformation describe-stacks --stack-name $(STACKNAME)

delete-stack:
	$(AWS) cloudformation delete-stack --stack-name $(STACKNAME)
	$(AWS) cloudformation wait stack-delete-complete --stack-name $(STACKNAME)

list-stacks:
	aws cloudformation describe-stacks --query="Stacks[].StackName" --output=table

pip:
	pip install --quiet --upgrade --requirement requirements.txt

.PHONY: lint clean stack describe-stack delete-stack ssh regionmap list-stacks pip
