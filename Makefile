venv_dir=local/venv
pyvenv=pyvenv-3.7

default: check

check: $(venv_dir)/packages-installed
	$(venv_dir)/bin/py.test tests
	
run: $(venv_dir)/packages-installed
	$(venv_dir)/bin/mqttclient

$(venv_dir)/packages-installed: requirements.txt
	test -d $(venv_dir) || $(pyvenv) $(venv_dir)
	$(venv_dir)/bin/pip install -U pip
	$(venv_dir)/bin/pip install -r requirements.txt
	$(venv_dir)/bin/pip install -e .
	touch $@