FROM python:3.9.1-slim-buster

RUN pip install pandas sklearn
# COPY validate.py /usr/local/bin/.
COPY score.py /usr/local/bin/.
RUN chmod +wx /usr/local/bin/*.py
# RUN cd /usr/local/bin/