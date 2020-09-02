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
	@curl https://blob-eu-central-1-nwsekq.s3.eu-central-1.amazonaws.com/sara/7a/7ac3/7ac3f6b6-46e0-442e-a218-efd91f8d7952.bin?response-content-disposition=attachment%3B%20filename%3D%22Codoxer-20200902T082109Z-001.zip%22&response-content-type=application%2Fzip&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAI75SICYCOZ7DPWTA%2F20200902%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20200902T130954Z&X-Amz-SignedHeaders=host&X-Amz-Expires=1800&X-Amz-Signature=1afc91159aab8a5ad246865bdcf5cd6d21c501483882b8e79a9f8ffcad4c432b > models.zip
	@mv models.zip codoxer/models/models.zip
	@cd codoxer/models; tar xvf models.zip; rm models.zip;
	@cd codoxer/models/Codoxer; mv -f trained_model_132 selector_132 user_id_dict_132.json vectorizer_132 ..


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
