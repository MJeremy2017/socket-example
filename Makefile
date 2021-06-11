docker-build:
	docker build -t server-client .

docker-run:
	docker run -it server-client