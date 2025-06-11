FROM python:3.11
ENV PYTHONUNBUFFERED=1
ENV CASS_HOST=cassandra
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install wait-for-it

RUN mkdir /code
WORKDIR /code
RUN pip install poetry
ADD . /code/
RUN poetry config virtualenvs.in-project true
RUN poetry install --with dev

EXPOSE 8000
