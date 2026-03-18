import math
import matlab.engine
from bayes_opt import BayesianOptimization

# 1. Start MATLAB engine ONCE globally to avoid massive overhead during optimization iterations
print("Starting MATLAB engine... (this may take a few seconds)")
eng = matlab.engine.start_matlab("-nodisplay") 
eng.addpath("/Users/akhilpatel/Desktop/Dissertation/WFSim-master")
print("MATLAB engine started successfully.")

def objective_function(yaw_angle):
    """
    Calls the MATLAB function WFSim_simulation_use and returns the total average power.
    """
    print(f"Evaluating yaw angle: {yaw_angle}")
    try:
        # Cast to standard python float so MATLAB engine parses it correctly as a double
        yaw_val = float(yaw_angle)
        
        # Call MATLAB function (which now returns a double natively)
        total_avg_power = eng.WFSim_simulation_use(yaw_val)  
        
        # Safeguard: Check if MATLAB returned NaN or Inf
        if math.isnan(total_avg_power) or math.isinf(total_avg_power):
            print(f"Warning: Yaw angle {yaw_angle} resulted in NaN/Inf. Penalizing.")
            return -1e9

        print(f"Yaw angle {yaw_angle} -> Total Avg Power: {total_avg_power}")
        return total_avg_power  

    except Exception as e:
        print(f"Error evaluating yaw angle {yaw_angle}: {e}")
        # Return a heavily penalized score if the simulation fails so the optimizer avoids this region
        return -1e9  

def optimize_yaw():
    """
    Optimization function to find the best yaw angle using Bayesian Optimization.
    """
    optimizer = BayesianOptimization(
        f=objective_function,
        pbounds={"yaw_angle": (-30, 30)},  
        verbose=2,  
        random_state=42  
    )

    # Run optimization
    optimizer.maximize(
        init_points=5,  
        n_iter=20  
    )

    print(f"Best result: {optimizer.max['params']} -> {optimizer.max['target']}")


if __name__ == "__main__":
    try:
        optimize_yaw()
    finally:
        # 2. Ensure the MATLAB engine safely quits when the script ends or errors out
        print("Closing MATLAB engine...")
        eng.quit()
        print("Engine closed.")
