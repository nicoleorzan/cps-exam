### Temperature control for a Chemical Batch Reactor via PID controllers and RL


In this repository you can find the analysis of the temperature variation for a Chemical Batch Reactor.

* ```BatchReactor.py``` is a class containing variables and the dynamics of the Reactor
* ```Simple_PID.py``` is a class containing a a simple implementation of a **PID controller**<sup>1</sup> (you don't say?)
* ```PID_Loop.py``` contains the application of the PID to the Reactor
* ```main.py``` launches the PID
* ```STL.py``` contains the expression and evaluation of **Signal Temporal Logic** requirements over the reactor temperature variable<sup>2</sup>
* ```trace_statistics.py``` contains the Falsification of requirementd over a sample of trajectories with noise
* ```ReinforcementLearning.py``` is a class containing the definition of sates, actions and rewards to perform Reinforcement Learning
* ```rl_train_test.py``` launches a Reinforcement Learning code with **SARSA** evaluation policy to follow the constant signal

Some Results:

Reactor temperature following a varying signal.
<figure>
  <img src="Images/reactor_temperature.png" width=500px>
</figure>

Reactor temperature variation following the policy obtained from SARSA.
<figure>
  <img src="Images/rl_output.png" width=500px>
</figure>

### References:

1) A. Shamekh, T. Hussein, and A. Altowati, "Design of Standard PID Controller for Exothermic Batch Process Simulation", 2013 European Modelling Symposium.

2) Temporal Logic package: https://github.com/mvcisback/py-metric-temporal-logic
