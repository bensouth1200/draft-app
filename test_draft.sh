#!/bin/bash

for x in {0..200}
do
	echo "Draft $x starting"
	draft single

	if [ $? -ne 0 ]
	then
		echo "Draft $x: FAILURE!" >> results.txt
		exit 1
	else
		echo "Draft $x: SUCCESS!" >> results.txt
	fi
done
