import matlab.engine
from bayes_opt import BayesianOptimization

# Define the objective function to maximize
def objective_function(yaw_angle):
    """
    Calls the MATLAB function WFSim_simulation_use and returns the total average power.
    :param yaw_angle: The yaw angle to pass to WFSim_simulation_use.
    :return: Total average power output from WFSim_simulation_use.
    """
    print(f"Evaluating yaw angle: {yaw_angle}")
    try:
        # MATLAB setup
        eng = matlab.engine.start_matlab("-nodisplay") 
        eng.addpath("/Users/akhilpatel/Desktop/Dissertation/WFSim-master")

        # Call MATLAB function
        total_avg_power = float(eng.WFSim_simulation_use(yaw_angle))  # Ensure this returns a Python float

        eng.quit()  # Close MATLAB engine
        print(f"Yaw angle {yaw_angle} -> Total Avg Power: {total_avg_power}")
        return total_avg_power  # Return total average power
    except Exception as e:
        print(f"Error evaluating yaw angle {yaw_angle}: {e}")
        eng.quit()
        return None

# Initialize Bayesian Optimization
def optimize_yaw():
    """
    Optimization function to find the best yaw angle using Bayesian Optimization.
    It maximizes total average power returned by WFSim_simulation_use.
    """
    optimizer = BayesianOptimization(
        # Bounds of the parameter; here yaw_angle is between 0 and 30 degrees (example bounds)
        f=objective_function,
        pbounds={"yaw_angle": (-30, 30)},  # Update bounds based on your yaw angle limits
        verbose=2,  # Verbose for logging
        random_state=42  # Ensures reproducibility
    )

    # Run optimization
    optimizer.maximize(
        init_points=5,  # Number of initial points to explore randomly (default is 5)
        n_iter=20  # Number of iterations for optimisation (default is 20)
    )

    # Best result
    print(f"Best result: {optimizer.max['params']} -> {optimizer.max['target']}")


if __name__ == "__main__":
    optimize_yaw()
