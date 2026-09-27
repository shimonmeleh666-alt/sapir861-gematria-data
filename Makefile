reproduce:
	python3 reproduce.py
docker:
	docker build -t sapir861-repro . && docker run --rm sapir861-repro
