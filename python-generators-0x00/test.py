#!/usr/bin/python3
import sys
from itertools import islice

# Import the module
processing = __import__('1-batch_processing')

##### Print processed users in a batch of 50
try:
    # Get the generator function from the module
    batch_gen = getattr(processing, 'batch_processing')

    # Iterate over the generator and print each user
    for user in islice(batch_gen(50), 10):  # limit to first 10 for readability
        print(user)

except BrokenPipeError:
    sys.stderr.close()
