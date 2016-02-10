Error Correcting
================

This library aims to create a powerful error correcting framework by:

 - catching exceptions
 - extracting traceback
 - disassemble frames' code
 - analyze bytecode to try to find the origin of exceptions (supplied data, or wrong algorithm)
 - try to modify bytecode according to a set of predefined possible resolutions
 - if a resolution is found, validate the modified bytecode and continue the execution without raising error
 - if no resolution is found, re-raise the error

Status
------

This project is actually in the specification phase:

 - no concrete work is done
 - API draft is being written
 - analysis process is being discussed

License
-------

This project is released under the **MIT** license. See the ``LICENSE`` file for more information.