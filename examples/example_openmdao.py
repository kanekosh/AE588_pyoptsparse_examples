import numpy as np
import openmdao.api as om


def run_optimization(optimizer='SQP'):
    """
    optimzier = 'SQP' or 'IPOPT'
    """

    # build the model
    prob = om.Problem()

    prob.model.add_subsystem('paraboloid', om.ExecComp('f = (x-3)**2 + x*y + (y+4)**2 - 3 + z**2'), promotes=['*'])
    prob.model.add_subsystem('lincon1', om.ExecComp('hlin1 = x + y'), promotes=['*'])
    prob.model.add_subsystem('lincon2', om.ExecComp('hlin2 = x + 2 * y'), promotes=['*'])
    prob.model.add_subsystem('nonlcon1', om.ExecComp('hnl1 = x**2'), promotes=['*'])
    prob.model.add_subsystem('nonlcon2', om.ExecComp('hnl2 = x**2 + y**2'), promotes=['*'])

    # setup optimizer
    prob.driver = om.pyOptSparseDriver()
    prob.driver.options['print_results'] = True

    if optimizer == 'SQP':
        # use my SQP
        prob.driver.options['optimizer'] = 'SQP'
        # options
        prob.driver.opt_settings['tol_opt'] = 1e-6
        prob.driver.opt_settings['tol_feas'] = 1e-6
        prob.driver.opt_settings['max_iter'] = 500   # max major iterations
        prob.driver.opt_settings['hessian_reset_freq'] = 100   # reset Hessian every this many iterations
        prob.driver.opt_settings['num_threads'] = 1   # number of threads for Gurobi's QP solver

    elif optimizer == 'IPOPT':
        # use IPOPT
        prob.driver.options['optimizer'] = 'IPOPT'
        # options
        prob.driver.opt_settings['max_iter'] = 500
        # prob.driver.opt_settings['alpha_for_y'] = 'safer-min-dual-infeas'
        prob.driver.opt_settings['print_level'] = 5
        # prob.driver.opt_settings['nlp_scaling_method'] = 'gradient-based'
        prob.driver.opt_settings['nlp_scaling_method'] = 'none'
        prob.driver.opt_settings['tol'] = 1e-6   # relative tolerance
        prob.driver.opt_settings['dual_inf_tol'] = 1e-6   # absolute optimality
        prob.driver.opt_settings['constr_viol_tol'] = 1e-6   # absolute constraint violation
        prob.driver.opt_settings['hessian_approximation'] = 'limited-memory'
        prob.driver.opt_settings['limited_memory_max_history'] = 100
        # prob.driver.opt_settings['mu_init'] = 1e-1   # should start from 1e-6 when not optimizing the design (i.e. initial guess is very close to optimum)
        # prob.driver.opt_settings['mu_strategy'] = 'monotone'
        prob.driver.opt_settings['bound_mult_init_method'] = 'mu-based'
        prob.driver.opt_settings['max_resto_iter'] = 100

    else:
        raise RuntimeError('Optimizer not recognized')

    # define optimization problem
    prob.model.add_design_var('x', lower=-100, upper=100)
    prob.model.add_design_var('y', lower=-100, upper=100)
    prob.model.add_design_var('z', lower=-100, upper=100)
    prob.model.add_objective('f')
    # linear constraints
    prob.model.add_constraint('hlin1', equals=2., linear=True)
    prob.model.add_constraint('hlin2', lower=-10, upper=10., linear=True)
    # nonlinear constraints
    prob.model.add_constraint('hnl1', equals=2, linear=False)
    prob.model.add_constraint('hnl2', lower=0.1, upper=100, linear=False)
    # prob.model.add_constraint('h', lower=0.5, upper=1.5)

    prob.setup()

    # Set initial values.
    prob.set_val('x', 3.0)
    prob.set_val('y', -4.0)
    prob.set_val('z', 1.0)

    # run the optimization
    prob.run_driver()

    print('\n\nOptimizer:', optimizer)
    print('x_opt =', prob.get_val(name='x')[0])   # 1.41421356
    print('y_opt =', prob.get_val(name='y')[0])   # 0.58578644
    print('z_opt =', prob.get_val(name='z')[0])   # 0
    print('f_opt =', prob.get_val(name='f')[0])   # 21.372583


if __name__ == '__main__':
    print('============ IPOPT ============')
    run_optimization(optimizer='IPOPT')

    print('\n\n\n============ SQP ============')
    run_optimization(optimizer='SQP')