FROM python:3.10.18-slim
RUN apt-get update && \
    apt-get install -y libpq-dev gcc
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "run.py"]