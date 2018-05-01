# Install pytest python library as well as add all files in current directory
FROM python:alpine AS base
WORKDIR /usr/src/app

# Copy the cloud plugin source files to the plugin directory
RUN pip3 install --upgrade pip==9.0.*

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./
RUN ENV_NAME=testing coverage run --source="curaDrivePlugin" -m pytest
RUN coverage report --skip-covered --show-missing --fail-under=0
