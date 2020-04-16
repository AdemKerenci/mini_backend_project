app.test:
	docker exec music-proj-app python3 tests/test.py -H localhost -P 5000 --add-data