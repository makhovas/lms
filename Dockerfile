FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir lms

WORKDIR lms

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .


RUN chmod a+x docker/*.sh