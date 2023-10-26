# Note for GSI (not relevant to students)

### Prepare a Docker image
1. Start from an mdolab public image
    ```
    $ docker pull mdolab/public:u22-gcc-ompi-stable`.
    ```
    TODO: prepare AMD64 image?
2. Create a container
    ```
    $ docker run -it --name AE588_pyoptsparse_XXX mdolab/public:u22-gcc-ompi-stable /bin/bash
    ```
3. Exit a container: `$ exit`
4. Restart a container
    ```
    docker start AE588_pyoptsparse_XXX
    docker exec -it AE588_pyoptsparse_XXX /bin/bash
    ```

### In a Docker container
1. Install my fork of pyOptSparse
    ```
    git clone --branch sqp https://github.com/kanekosh/pyoptsparse.git
    cd pyoptsparse
    pip install -e .
    ```
2. Install my fork of OpenMDAO
    ```
    git clone --branch sqp_wrapper https://github.com/kanekosh/OpenMDAO.git
    cd OpenMDAO
    pip install -e .
    ```
3. Install SQP dependencies
    ```
    pip install cvxpy-base==1.3.2 gurobipy==10.0.2
    ```
4. Download example scripts:
    ```
    git clone https://github.com/kanekosh/AE588_pyoptsparse_project.git
    ```
 
### Transfer image