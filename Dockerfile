FROM python:3.7
WORKDIR /app
COPY receiver.py .
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
CMD ["python", "/app/receiver.py"]



