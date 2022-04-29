if [ -n "$1" ]
then
  while sleep 1 ; do find ./clitodoapp ./tests -name '*.py' | entr -d pytest $1; done
else
  while sleep 1 ; do find ./clitodoapp ./tests -name '*.py' | entr -d pytest ; done
fi
