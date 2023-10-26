# Fall 2023 AE588 pyOptSparse project

## Installation

### Docker
The easiest way to run pyOptSparse is to use a Docker image provided by the GSI, which already installs pyOptSparse, OpenMDAO, and other dependencies.  
You can also install them natively on Linux or Mac, but you're on your own.
Check [pyOptSparse documentation](https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest/install.html) if you wish to install it by yourself. You'll need to install my fork of pyOptSparse, my fork of OpenMDAO, cvxpy, and Gurobi.


### Mounting Gurobi license



## Examples
- `AE588_pyoptsparse_project/examples/example_openmdao.py`: OpenMDAO runscript to optimize a toy problem using IPOPT and my SQP.
- `AE588_pyoptsparse_project/examples/example_pyoptsparse.py`: pyOptSparse runscript to optimize the sane toy problem using IPOPT and my SQP.

## SQP code
The SQP code is available in `/repos/pyoptsparse/pyoptsparse/pySQP/sqp.py` in the docker container.  
Feel free to modify the SQP code if needed.
Please let me know if you find a bug or any issue (I'm pretty sure there are bugs)!

The same code can be viewed [on GitHub](https://github.com/kanekosh/pyoptsparse/blob/sqp/pyoptsparse/pySQP/sqp.py).
See `_set_options` method for the list of options and the default values.
