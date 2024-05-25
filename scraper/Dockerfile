# scraper/Dockerfile

FROM python:3.11.5-slim

WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scraper.py .

CMD ["python", "scraper.py"]
