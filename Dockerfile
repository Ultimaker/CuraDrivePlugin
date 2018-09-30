FROM python:3.6-alpine AS base
WORKDIR /usr/src/app

RUN pip3 install CuraPackageDeployer

CMD ["python3", "deploy.py"]
ADD . .
