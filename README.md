### Cyber-Physical Systems exam Repository

Studying the behavior of a Chemical Batch Reactor.


## 1) PID control<sup>1</sup>

Controlling the system with a simple pid control.

<figure>
  <img src="Images/reactor_temperature1.png" width=500px>
  <figcaption>
      Reactor temperature following a constant signal
  </figcaption>
</figure>


<figure>
  <img src="Images/reactor_temperature.png" width=500px>
  <figcaption>
      Reactor temperature following a varying signal
  </figcaption>
</figure>

## 2) Defining Signal Temporal Logic requirement<sup><2/sup>



## 3) Controlling the system with Reinforcement Learning

Learning made by SARSA algorithm.

States discretization:
* 19 slices for $T_{jsp}$, from 20 to 120
* 15 slices for $T_{R}$, from 20 to 140

State: tuple $(T_C, T_R)$ 

Three possible actions for each state: increase $T_{jsp}$, decrease $T_{jsp}$, keep the same $T_{jsp}$

Q matrix dimension = 19 $\times$ 5

Output:

<figure>
  <img src="Images/rl_output.png" width=500px>
  <figcaption>
      Reactor temperature policy obtained from SARSA.
  </figcaption>
</figure>

## References:

1) A. Shamekh, T. Hussein, and A. Altowati, "Design of Standard PID Controller for Exothermic Batch Process Simulation", 2013 European Modelling Symposium.

2) Temporal Logic package: https://github.com/mvcisback/py-metric-temporal-logic
