# run runs manage.py runserver
# exec runs manage.py [c=COMMAND]
# startapp runs manage.py startapp [t=TARGET]
# migrate runs manage.py migrate [t=TARGET] [i=INDEX]
# fake runs manage.py migrate [t=TARGET] [i=INDEX] --fake
# makemigrations runs manage.py makemigrations [t=TARGET]
# merge runs manage.py makemigrations [t=TARGET] --merge
# beat runs celery -A synergy beat -l [l=LOG_LEVEL]
# worker runs celery -A synergy worker [WORKER_POOL] -l [l=LOG_LEVEL]

.PHONY: run exec startapp migrate makemigrations merge fake beat worker
.DEFAULT_GOAL := run

PYTHON       = python
COMMAND     ?=
TARGET      ?=
INDEX       ?=
LOG_LEVEL   ?=
WORKER_POOL ?=

ifeq ($(OS),Windows_NT)
	WORKER_POOL = --pool solo
else
	PYTHON = python3
endif

ifdef c
	COMMAND = ${c}
endif

ifdef t
	TARGET = ${t}
endif

ifdef i
	INDEX = ${i}
endif

ifdef l
	LOG_LEVEL = ${l}
else
	LOG_LEVEL = INFO
endif

run:
	${PYTHON} product/manage.py runserver

exec:
	${PYTHON} product/manage.py ${COMMAND}

startapp:
	${PYTHON} product/manage.py startapp ${TARGET}

migrate:
	${PYTHON} product/manage.py migrate ${TARGET} ${INDEX}

fake:
	${PYTHON} product/manage.py migrate ${TARGET} ${INDEX} --fake

makemigrations:
	${PYTHON} product/manage.py makemigrations ${TARGET}

merge:
	${PYTHON} product/manage.py makemigrations ${TARGET} --merge

beat:
	celery -A synergy beat -l ${LOG_LEVEL}

worker:
	celery -A synergy worker ${WORKER_POOL} -l ${LOG_LEVEL}
