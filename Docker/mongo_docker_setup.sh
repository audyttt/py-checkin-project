#!/bin/bash
docker pull mongo
docker run -d -p 27017:27017 --name mongodb mongo
