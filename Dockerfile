FROM python:2.7
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD requirements-dev.txt /code/
RUN pip install -r requirements-dev.txt
ADD . /code/
RUN python setup.py develop

EXPOSE 8000
