# Note for GSI (not relevant to students)

## Docker image preparation

### Create a container
1. Start from an mdolab public image
    ```
    $ docker pull --planform linux/arm64 mdolab/public:u22-gcc-ompi-stable`
    ```
    NOTE: Set `--planform linux/amd64` or `--planform linux/arm64` (for M2 Mac)
2. Create a container
    ```
    $ docker run -it --name AE588_pyoptsparse_XXX mdolab/public:u22-gcc-ompi-stable /bin/bash
    ```
3. Restart a container later
    ```
    docker start AE588_pyoptsparse_XXX
    docker exec -it AE588_pyoptsparse_XXX /bin/bash
    ```

### Install stuff in the container
1. Update numpy and scipy versions
    ```
    pip install numpy==1.25.2 scipy==1.10.1
    ```

2. Install my fork of pyOptSparse
    ```
    cd repos/pyoptsparse
    git remote add kanekosh https://github.com/kanekosh/pyoptsparse.git
    git checkout -b sqp
    git config pull.rebase false
    git pull kanekosh sqp
    pip install -e .
    ```
3. Install my fork of OpenMDAO
    ```
    cd repos
    git clone --branch sqp_wrapper https://github.com/kanekosh/OpenMDAO.git
    cd OpenMDAO
    pip install -e .
    ```
4. Install SQP dependencies
    ```
    pip install cvxpy-base==1.3.2 gurobipy==10.0.2
    ```
5. Download example scripts:
    ```
    cd ..
    git clone https://github.com/kanekosh/AE588_pyoptsparse_project.git
    ```
6. Run examples
    ```
    cd AE588_pyoptsparse_project/examples
    python examples_pyoptsparse.py
    python examples_openmdao.py
    ```
    NOTE: Gurobi will run under the restricted license, which can only solve small-scale problems. For large problems, we need an academic license in the host machine and mount it to the Docker container.
 
### Create an image from the modified container
1. Create an image from the container above
    ```
    $ docker commit AE588_pyoptsparse_XXX kanekosh/ae588public:arm64
    ```
    This will create an image named "ae588public" with tag "arm64".
2. Test the new image
    ```
    docker run -it --name test_container kanekosh/ae588public:arm64 /bin/bash
    ```
    TODO: test mounting Gurobi license
3. Push to DockerHub
    ```
    docker push kanekosh/ae588public:arm64
    ```
    This will push the image to https://hub.docker.com/u/kanekosh/ae588public
