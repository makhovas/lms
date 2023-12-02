#!/bin/bash

sleep 15

celery -A lms.celery worker -l INFO -S django