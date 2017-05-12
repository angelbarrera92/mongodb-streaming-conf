#!/bin/bash

USER=${MONGODB_USER:-"admin"}
DATABASE=${MONGODB_DATABASE:-"admin"}
PASS=${MONGODB_PASS:-"admin123"}
CAPPED_COLLECTION=${MONGODB_CAPPEDCOLLECTION:-"no"}
CAPPED_COLLECTION_NAME=${MONGODB_CAPPEDCOLLECTION_NAME:-"streaming"}
CAPPED_COLLECTION_SIZE=${MONGODB_CAPPEDCOLLECTION_SIZE:-25600}
CAPPED_COLLECTION_MAX=${MONGODB_CAPPEDCOLLECTION_MAX:-100}
_word=$( [ ${MONGODB_PASS} ] && echo "preset" || echo "random" )

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MongoDB service startup"
    sleep 5
    mongo admin --eval "help" >/dev/null 2>&1
    RET=$?
done

echo "=> Creating an ${USER} user with a ${_word} password in MongoDB"
mongo admin --eval "db.createUser({user: '$USER', pwd: '$PASS', roles:[{role:'root',db:'admin'}]});"

if [ "$DATABASE" != "admin" ]; then
    echo "=> Creating an ${USER} user with a ${_word} password in MongoDB"
    mongo admin -u $USER -p $PASS << EOF
use $DATABASE
db.createUser({user: '$USER', pwd: '$PASS', roles:[{role:'dbOwner',db:'$DATABASE'}]})
EOF
fi

if [ "$CAPPED_COLLECTION" == "yes" ]; then
	echo "=> Creating a capped collection named ${CAPPED_COLLECTION_NAME} with a size of ${CAPPED_COLLECTION_SIZE} bytes or ${CAPPED_COLLECTION_MAX} documents"
	mongo admin -u $USER -p $PASS << EOF
use $DATABASE
db.createCollection('$CAPPED_COLLECTION_NAME', { capped : true, size : $CAPPED_COLLECTION_SIZE, max : $CAPPED_COLLECTION_MAX } )
EOF
fi

echo "=> Done!"
touch /data/db/.mongodb_password_set

echo "========================================================================"
echo "You can now connect to this MongoDB server using:"
echo ""
echo "    mongo $DATABASE -u $USER -p $PASS --host <host> --port <port>"
echo ""
echo "Please remember to change the above password as soon as possible!"
echo "========================================================================"