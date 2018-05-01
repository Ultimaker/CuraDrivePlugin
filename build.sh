#!/usr/bin/env bash
# Copyright (c) 2018 Ultimaker B.V.

# This script builds the docker image for this project in order to run the tests.

GIVEN_TAG=$1

if [ -z $GIVEN_TAG ]; then
    TAG="cura-drive-plugin"
    echo "No image tag given, running project and its dependencies locally"
else
    TAG=$GIVEN_TAG
    echo "An image with tag $GIVEN_TAG will be created"
fi

docker build --tag $TAG . 2>&1
