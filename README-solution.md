```
Description of files in this directory:
.
├── docs.txt           # file containing documentation extrapolated from example
├── filter.py            # python script that filters STDIN, outputs to STDOUT
├── unittests.py       # unittests
├── tests
│   ├── example_input  # the original example file
│   ├── example_output # the original example output
└── test.sh            # shell script to run filter.py against sample text
```

To run the filter:
```
    cat input_file | python filter.py

    or

    python filter.py < input_file
```

To run the unittests:
```
    python test.py
```

To run a bash script to check the filter against the original input
and output example:
```
    bash unittests.sh
```

Tested on Ubuntu 8.10
