#!/bin/bash

# run the example text through the filter
python filter.py < tests/example_input > /tmp/tmp.out


DIFF_OUTPUT="$(diff /tmp/tmp.out tests/example_output)"

# if no diff from expected output, print ok
# else print a diff with the line numbers and differences
if [ "$DIFF_OUTPUT" = "" ]; then
   echo "output ok";
else
   sdiff -l /tmp/tmp.out tests/example_output | cat -n | grep -v -e '($'
fi
