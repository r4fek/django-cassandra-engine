FROM python:3.7
ENV PYTHONUNBUFFERED=1
ENV CASS_HOST=cassandra
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD requirements-dev.txt /code/
RUN pip install -r requirements-dev.txt
ADD . /code/
RUN pip3 install -e .

EXPOSE 8000
