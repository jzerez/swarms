# Swarms
**ENGR3590: A Computational Introduction to Robotics, Olin College of Engineering, FA2020**

*Nathan Estill, Jonathan Zerez*

<br />

In this project, we set out to create a simulated decentralized robot swarm that would exhibit self-assembling properties. Specifically, we wanted to replicate morphogenesis, the process by which cells are able to self-organize themselves in order to form complex tissues and organs through local interactions alone. This is of great interest to us, as decentralized systems are full of complexity, and are quite different from centralized robotic systems. Decentralized swarms offer a number of really cool advantages in that they are very robust to external noise, damage to a number of individual agents within the swarm, and unpredictable variations in the environment. 

If you would like to read more, check out [the website](https://jzerez.github.io/swarms/writeups/mainpage/main.md)


For reference, we have also created an important demo video for the project, which can be found [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ).

## To Run

```
python3 Simulator.py
```
If you want to change parameters yourself, change the parameters at the bottom of Simulator.py. The parameters are, in order:
* `nSteps`: the number of time steps the simulation will run for
* `gridSize`: the overall size of the space the robots will be in
* `rdParams`: a tuple, with the following:
    * `cA`: the diffusion ratio of A
    * `cB`: the diffusion ratio of B
    * `a_add_rate`: the amount of A to add at each step
    * `b_add_rate` add rate: the amount of B to add at each step (usually negative to remove B)
* `sideLength`: the length of the side of the square of robots, or diameter if a circle
* `stepsPerFrame`: the number of time steps between each captured frame of the animation
* `stepsPerChemicalUpdate`: the number of time steps between when the robots update their chemical concentration
* `stepsPerRobotMovement`: the number of time steps between when the robots move

As a potential starting point for the `rdParams`, the values `(0.43,0.19,0.035,-0.1)` will give polka-dots, and the values `(0.5,0.25,0.06,-0.124)` will give a worm.

### Dependencies

* `numpy`
* `matplotlib`
* `scipy`