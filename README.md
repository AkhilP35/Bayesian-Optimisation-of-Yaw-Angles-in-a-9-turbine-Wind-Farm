# Bayesian Optimization of Yaw Angles in a 9-Turbine Wind Farm

This project applies Bayesian Optimization to find the optimal yaw angles for a 9-turbine wind farm, aiming to maximize the total average power output. The optimization loop is driven by Python using the `bayes_opt` library, which interfaces directly with a MATLAB-based Wind Farm Simulator (WFSim) to evaluate the power output for different yaw configurations.

## Project Structure

- **`Bayesian Optimization.py`**: The main Python script that initializes the Bayesian Optimizer and manages the global MATLAB engine.
- **`WFSim_simulation_use.m`**: The MATLAB script that runs the WFSim environment for a given set of yaw angles and calculates the total average power output over the simulation period.

## Prerequisites

To run this project, you need:
- Python 3.x
- MATLAB (with a valid license)
- [MATLAB Engine API for Python](https://uk.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)
- [The Bayesian Optimization Python package](https://github.com/bayesian-optimization/BayesianOptimization)
- The [WFSim repository](https://github.com/TUDelft-DataDrivenControl/WFSim) cloned locally and path updated in the Python script.


## Iterative Code Improvements

Throughout the development of this project, several significant improvements were made to ensure both the physical accuracy of the simulation and the computational efficiency of the optimization loop.

### 1. Wake Propagation Delay (Physics Logic)
Initially, the average power was calculated from the very first timestep. However, wind turbine wakes take time to travel downstream and affect the other turbines. 
- **Improvement:** The MATLAB script was updated to ignore the first 35 timesteps. The average power is now only calculated from timestep 36 onwards (`mean(total_power_history(36:end))`). This allows the wakes to fully propagate, giving the Bayesian Optimizer realistic, steady-state data to evaluate.

### 2. Full Simulation Length
- **Improvement:** A hardcoded limit of `NN = 100` was removed, allowing the WFSim simulation to run for its full, default length of `NN = 998` timesteps. This ensures that the optimization evaluates long-term farm performance rather than a brief snapshot.

### 3. True Average Power Calculation
- **Improvement:** The original MATLAB script only calculated the total power at the *final* timestep and returned it as a string. It was updated to track the power output at every single timestep into an array (`total_power_history`), calculate the true average mathematically, and return it natively as a `double` so Python can process it without string parsing errors.

### 4. Global MATLAB Engine Initialization (Python Speed Optimization)
Starting the MATLAB engine takes several seconds. Originally, the engine was being started and stopped *inside* the objective function, meaning the overhead was suffered on every single Bayesian optimization iteration.
- **Improvement:** The MATLAB engine initialization (`matlab.engine.start_matlab()`) was moved to the global scope of the Python script. It now starts only once at the beginning of the script and remains open, drastically speeding up the overall execution time of the optimizer.

### 5. Disabled Visuals and Verbose Outputs (MATLAB Speed Optimization)
To further reduce overhead and allow the simulation to run as fast as possible in the background, all graphical animations and console printouts inside WFSim were disabled.
- **Improvement:** The following simulation options were explicitly set to `0`:
  ```matlab
  verboseOptions.printProgress = 0;    
  verboseOptions.Animate       = 0;   
  verboseOptions.plotMesh      = 0;
  ```

## Usage

1. Update the WFSim path in `Bayesian Optimization.py` to point to your local installation:
   ```python
   eng.addpath("/Path/To/Your/WFSim-master")
   ```
2. Run the Python script:
   ```bash
   python "Bayesian Optimization.py"
   ```
3. The script will start the MATLAB engine, run the Bayesian Optimization over 25 iterations (5 initial random points + 20 optimization steps), and output the best yaw angle configuration found.
