## Planetary Orbiting and Scattering Sim
This program dynamically simulates $n$ planets in two dimensions, initialized with random dimensions, mass and velocity, moving in each others gravitational potential. For each timesteps the their new velocity and position is calculated using a forward Euler method. <br>
The planets are displayed on a pygame interface. The interface is always centered on the systems center of mass.<br>
Once the program is running you can create a new system by pressing the "right" arrow button on your keyboard.<br <br>
It is possible to change the number of planets simulated, by changing the variable ``n_planets`` in ``Scattering.py``. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/126679979/222162430-b1a5acc8-16ba-4f55-8469-a4727c3b8460.gif" alt="planets"/>
</p>
