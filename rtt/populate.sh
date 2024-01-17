#!/bin/bash

if [[ $* ]]
then
  ./manage.py search_index --populate -f --models $*
else
  ./manage.py search_index --populate -f
fi