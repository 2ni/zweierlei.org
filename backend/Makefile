.PHONY: init clean server tests shell

# If the first argument is "run"...
# http://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
ifeq (tests,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

# -U upgrade
install:
	pip install -Ur requirements.txt

clean:
	find . -name '*.pyc' -delete

server:
	python manage.py runserver --host 0.0.0.0

shell:
	python shell.py

# -f --failfast stop test on first failure
# -b --buffer   output during passing test is discarded
# make tests test=Test.test_user_update to run a single test
tests:
	python tests.py -f $(test)

populateDB:
	@cat redis.txt | redis-cli
	@rm -rf app/static/uploads
