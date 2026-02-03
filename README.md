# Bayesian-Optimisation-of-Yaw-Angles-in-a-9-turbine-Wind-Farm
Bayesian Optimisation of Yaw Angles in a 9 turbine Wind Farm

First Run (5 inital points 25 iterations):
Best result: {'yaw_angle': np.float64(0.5858817557635484)} -> 104610772.9763

Second Run (yaw angle boundary changed to -30 to 30, 6 initial points and 30 iterations):
Best result: {'yaw_angle': np.float64(0.07768900951580594)} -> 104624163.2324

Third Run (with 8 initial points and 40 iterations):
Best result: {'yaw_angle': np.float64(0.08635844528626278)} -> 104624161.9527


Used: https://github.com/bayesian-optimization/BayesianOptimization and https://github.com/TUDelft-DataDrivenControl/WFSim
