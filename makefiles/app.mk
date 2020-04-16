app.build:
	docker-compose build

app.up: 
	docker-compose up -d

app.stop:
	docker-compose down