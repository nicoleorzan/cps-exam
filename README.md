### Cyber-Physical Systems exam Repository


In this repository you can find the analysis of the temperature variation for a Chemical Batch Reactor.

* the class BatchReactor contains the variables and the dynamics of the Reactor
* the class Simple_PID contains a simple implementation of a PID controller (you don't say?)
* the class PID_Loop contains the application of the PID to the Reactor
* main.py launches the PID
* The file STL contains the xpression and evaluation of Signal Temporal Logic requirements<sup><2/sup> over the reactor temperature variable
* The file trace_statistics contains the Falsification of requirementd over a sample of trajectories with noise
* The class ReinforcementLearning contains the definition of variables and the selection of related actions
* main_rl launches a Reinforcement Learning code with SARSA evaluation policy to follow the constant signal

Some Results:

<figure>
  <img src="Images/reactor_temperature.png" width=500px>
  <figcaption>
      Reactor temperature following a varying signal
  </figcaption>
</figure>

<figure>
  <img src="Images/rl_output.png" width=500px>
  <figcaption>
      Reactor temperature policy obtained from SARSA.
  </figcaption>
</figure>

### References:

1) A. Shamekh, T. Hussein, and A. Altowati, "Design of Standard PID Controller for Exothermic Batch Process Simulation", 2013 European Modelling Symposium.

2) Temporal Logic package: https://github.com/mvcisback/py-metric-temporal-logic
