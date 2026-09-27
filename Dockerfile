FROM python:3.12-slim
WORKDIR /repro
COPY . /repro
CMD ["python", "reproduce.py"]
