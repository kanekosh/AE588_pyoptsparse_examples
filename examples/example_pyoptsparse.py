import numpy as np
from pyoptsparse import IPOPT, SQP, Optimization

# define function
def func(xdict):
    x = xdict["xvars"][0]
    y = xdict["xvars"][1]
    z = xdict["xvars"][2]

    # objective
    funcs = {}
    funcs["obj"] = (x - 3)**2 + x * y + (y + 4)**2 - 3 + z**2

    # constraints
    hlin1 = x + y
    hlin2 = x + 2 * y
    hnl1 = x**2
    hnl2 = x**2 + y**2

    funcs["con"] = np.array([hlin1, hlin2, hnl1, hnl2])
    fail = False

    return funcs, fail

def run_optimization(optimizer='SQP'):
    # Optimization Object
    optProb = Optimization("test problem", func)

    # Design Variables
    optProb.addVarGroup("xvars", 3, "c", lower=[-100, -100, -100], upper=[100, 100, 100], value=[3, -4, 1])

    # Constraints
    optProb.addConGroup("con", 4, lower=[2, -10, 2, 0.1], upper=[2, 10, 2, 100])

    # Objective
    optProb.addObj("obj")

    # setup optimizer
    if optimizer == 'SQP':
        # my SQP
        optOptions = {}
        optOptions['tol_opt'] = 1e-6
        optOptions['tol_feas'] = 1e-6
        optOptions['max_iter'] = 500   # max major iterations
        optOptions['hessian_reset_freq'] = 100   # reset Hessian every this many iterations
        optOptions['num_threads'] = 1   # number of threads for Gurobi's QP solver
        opt = SQP(options=optOptions)

    elif optimizer == 'IPOPT':
        # IPOPT
        optOptions = {}
        optOptions['max_iter'] = 500
        # optOptions['alpha_for_y'] = 'safer-min-dual-infeas'
        optOptions['print_level'] = 5
        # optOptions['nlp_scaling_method'] = 'gradient-based'
        optOptions['nlp_scaling_method'] = 'none'
        optOptions['tol'] = 1e-6   # relative tolerance
        optOptions['dual_inf_tol'] = 1e-6   # absolute optimality
        optOptions['constr_viol_tol'] = 1e-6   # absolute constraint violation
        optOptions['hessian_approximation'] = 'limited-memory'
        optOptions['limited_memory_max_history'] = 100
        # optOptions['mu_init'] = 1e-1   # should start from 1e-6 when not optimizing the design (i.e. initial guess is very close to optimum)
        # optOptions['mu_strategy'] = 'monotone'
        optOptions['bound_mult_init_method'] = 'mu-based'
        optOptions['max_resto_iter'] = 100
        opt = IPOPT(options=optOptions)

    else:
        raise RuntimeError('Optimizer not recognized')

    # run optimization
    sol = opt(optProb, sens="FD")
    # TODO / NOTE: I am lazy and I am doing FD here.
    # But you should provide the analytical derivatives using `sens` - please check pyOptSprase documentation to learn how to define gradient and Jacobians.
    # Also linear constraint requires special handing I think. In this example, I'm providing all lienar constraints as nonlinear. (Not sure if this slows down the optimization... maybe not. IPOPT probably doesn't support linear constraints but not sure about that too.)

    print(sol)


if __name__ == "__main__":
    print('============ IPOPT ============')
    run_optimization(optimizer='IPOPT')

    print('\n\n\n============ SQP ============')
    run_optimization(optimizer='SQP')