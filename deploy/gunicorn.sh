#!/bin/bash
NAME="paap"
DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
SOCKFILE=/tmp/gunicorn-paap.sock
LOGDIR=${DJANGODIR}/logs/gunicorn.log
USER=root
GROUP=root
NUM_WORKERS=10
DJANGO_WSGI_MODULE=PAAP.wsgi

rm -frv $SOCKFILE

cd $DJANGODIR
echo $DJANGODIR
echo $DJANGO_WSGI_MODULE

exec echo "paap-admin-server" | sudo -S ${DJANGODIR}/entorno/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGDIR
