FROM python:3.13.0
LABEL authors="Nvt5"

COPY src /src
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "src/pymusic.py"]