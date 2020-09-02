# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt
	@make get_tokenizer
	@make get_models

get_tokenizer:
	@curl -L https://github.com/dspinellis/tokenizer/archive/master.zip > master.zip
	@tar xvf master.zip
	@rm master.zip
	@cd tokenizer-master/src; make; make install
	@rm -rf tokenizer-master

get_models:
	@curl -L https://filetransfer.io/data-package/fW69C6mp/download > models.zip
	@mkdir codoxer/models
	@mv models.zip codoxer/models/models.zip
	@cd codoxer/models; tar xvf models.zip; rm models.zip;
	@cd codoxer/models/Codoxer; mv -f  selector_132 user_id_dict_132.json vectorizer_132 ..;mv trained_model_132 ../trained_model_132


check_code:
	@flake8 scripts/* codoxer/*.py

black:
	@black scripts/* codoxer/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit=$(VIRTUAL_ENV)/lib/python*

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr codoxer-*.dist-info
	@rm -fr codoxer.egg-info

install:
	@make install_requirements
	@pip install . -U

all: clean install test black check_code


uninstal:
	@python setup.py install --record files.txt
	@cat files.txt | xargs rm -rf
	@rm -f files.txt

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u lologibus2

pypi:
	@twine upload dist/* -u lologibus2
