FROM python:3.6-alpine AS base
WORKDIR /usr/src/app

# python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "deploy.py"]
ADD . .
