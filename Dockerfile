# syntax=docker/dockerfile:1

FROM python:3.10-slim
WORKDIR /flask

# copy code
COPY . .
RUN pip install --no-cache-dir flask

ENV FLASK_APP=app.py

# standard port for flask
EXPOSE 5000

# run cmd
CMD ["flask", "run", "--host=0.0.0.0"]
