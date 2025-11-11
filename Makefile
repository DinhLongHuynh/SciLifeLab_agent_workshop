.PHONY: *

build:
	docker build --force-rm=true -t scilifelab/ai-agents-ws .

run-jupyter-lab:
	# Start environment in jupyter notebook
	docker run -it --rm=true -p 2160:2160 -v .:/repo --name ai-agents-container scilifelab/ai-agents-ws

run-shell:
	# Start shell in running container
	docker exec -it ai-agents-container bash