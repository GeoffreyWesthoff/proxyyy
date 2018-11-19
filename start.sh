#!/bin/bash
gunicorn -w 4 -b 127.0.0.1:65534 proxy:app --worker-class sanic.worker.GunicornWorker
