FROM python:3.8-slim-buster

EXPOSE 5000 8000

COPY scripts/wait-for-it.sh /
RUN chmod 755 wait-for-it.sh

COPY requirements.txt /
RUN pip3.8 install -r requirements.txt

COPY brainz /brainz
