#!/bin/bash

if [[ $* ]]
then
  ./manage.py search_index --rebuild -f --models $*
else
  ./manage.py search_index --rebuild -f
fi