flake8: dev.flake8
black: dev.black
isort: dev.isort

build: app.build
up: app.up
stop: app.stop
test: app.test

include makefiles/dev.mk
include makefiles/app.mk
include makefiles/test.mk