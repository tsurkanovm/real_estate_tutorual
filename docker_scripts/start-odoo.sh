#!/bin/bash
set -e

echo "PYCHARM_DEBUG=$PYCHARM_DEBUG WAIT=$PYCHARM_DEBUG_WAIT"

if [ "$PYCHARM_DEBUG" = "1" ]; then
    export PYDEVD_PYCHARM_HOST="${PYCHARM_DEBUG_HOST:-host.docker.internal}"
    export PYDEVD_PYCHARM_PORT="${PYCHARM_DEBUG_PORT:-8888}"
    exec python3 -c "
import sys
sys.argv = ['odoo', '--config', '/etc/odoo/odoo.conf', '--dev', 'xml']
import pydevd_pycharm, os
pydevd_pycharm.settrace(os.environ['PYDEVD_PYCHARM_HOST'],
    port=int(os.environ['PYDEVD_PYCHARM_PORT']),
    suspend=os.environ.get('PYCHARM_DEBUG_WAIT','0')=='1',
    patch_multiprocessing=True)
import odoo.cli; odoo.cli.main()
"
else
    exec /usr/bin/odoo --config /etc/odoo/odoo.conf --dev xml
fi