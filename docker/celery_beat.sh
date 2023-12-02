#!/bin/bash

sleep 15

celery -A lms beat -l INFO -S django