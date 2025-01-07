#!/bin/bash

cd ./js || exit

~/.nvm/versions/node/v18.20.5/bin/npm run db:generate

cd .. || exit