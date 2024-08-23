FROM python:3.9.12-slim

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY script.py .

CMD [ "python", "script" ]

