#!/bin/bash
set -a # automatically export all variables
source .env
set +a
exec "$@"
