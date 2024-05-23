fla# Elasticsearch Search Tutorial

This directory contains a starter Flask project used in the Search tutorial.

## Tech stack:

- Python3.12
- Elasticsearch
- flask
- docker


## Setup:

1) Install elasticsearch locally using docker
	```bash
	docker run -p 9200:9200 -d --name elasticsearch \
	  -e "discovery.type=single-node" \
	  -e "xpack.security.enabled=false" \
	  -e "xpack.security.http.ssl.enabled=false" \
	  -e "xpack.license.self_generated.type=trial" \
	  docker.elastic.co/elasticsearch/elasticsearch:8.13.3
	```
 
2) Install python dependencies
	```bash
	pip install -r requirements.txt	
	```

3) run the project
	```bash
	flask run
	```

4) Index documents
	```bash
	flask reindex
	```

## Project formatting and Linting

1) Using ruff 
	```bash
	ruff format .
	ruff check .
	```
2) Using Black
	```bash
	black .
	```
3) Using isort
	```bash
	isort . --profile black
 	```