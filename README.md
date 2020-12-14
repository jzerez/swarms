# swarms
An investigation to decentralized swarming behavior in simple robotic agents.

## Resources
1. [TERMES](https://science.sciencemag.org/content/sci/343/6172/754.full.pdf?ijkey=wcGE/tKMM5iGM&keytype=ref&siteid=sci)
2. [TERMES Algorithm Paper](https://dash.harvard.edu/bitstream/handle/1/11213398/iros11wksp-werfel.pdf?sequence=1&isAllowed=y)
3. [Dynamic Organization of flocking behaviors in a large-scale boids model](https://link.springer.com/article/10.1007/s42001-019-00037-9)
4. [An overview on optimal flocking](https://arxiv.org/pdf/2009.14279.pdf)
5. [Morphogenesis in robot swarms](https://robotics.sciencemag.org/content/3/25/eaau9178)
6. [Programmable self-assembly in a thousand-robot swarm](https://science.sciencemag.org/content/345/6198/795.full)


### Dynamic Reconfiguration
I didn't look immensely into this one because it seemed a little too large and abstract. The flocking seemed like more of a reason to study biology than robotics.

### Third One

This one was similar to first, not much to say.

### Morphogenesis

I liked this one, it was pretty interesting. Seems pretty difficult, but could maybe try ourselves. The results didn't seem too promising though. It seemed like at the start they mentioned starfish shape, but all they ended up with were blobs with indents that seemed somewhat random.

* Based on Reaction-Diffusion equations
* Completely decentralized, no knowledge of intended final shape, no attempts to self-localize
* Much more nebulous and less application ready results
* Seems difficult to create useful metrics to classify swarm behavior/shapes
* Possible extension to make more extreme shapes?

### TERMES Algorithm paper
* A struct-path is a linear path through a top-down view of the desired final structure
* No branching or merging of pathes (yet... possible extension?)
* Defines a small set of rules that ensure impossible terrain isn't generated
* Agents know what the final shape should look like
* Agents need to localize themselves in the strcutre by finding and orienting to a known seed block

### 1000 Robot swarm
* Uses a set of four stationary agents as the "seed" to a given structure. Defines origin and orientation of axes
* Robots calculate gradient, basically distance to the origin expressed in the nearest number of robot-width units
* Robots are able to localize themselves based on local communication with other agents that have already successfully localized themselves within the frame and have stopped moving
* potential extension: have simultaneous movement? Kind of represents a huge departure from the original algorithm though. 

### Reaction Diffusion Overview
Reaction Diffusion is a term for when two chemicals that react together are left alone in an environment. The chemicals diffuse over time, and one of the chemicals react to form the other chemical. From this, different patterns can arise when different amounts of each chemical are added, or if each chemicals rate of diffusion is changed. 

### Paper Inspiration

For this project, we implemented the general principle behind this research paper about  [Morphogenesis in robot swarms](https://robotics.sciencemag.org/content/3/25/eaau9178). The paper had many kilobots performed reaction diffusion with each other with IR communications. They also would move along the edge if they were not close to a high chemical concentration. We wanted to reimplement this ourselves and try to get the robots to make interesting patterns.

### Simulation

We started with a simulation of many small robots in a space. The Robot class contains its chemical concentrations of A and B, its position, reaction diffusion parameters, and notable kernels. The robots are contained in a 2D grid, and can move to any of the eight surrounding grid spaces. Each robot also has access to each of its eight neighbors and their chemical concentration. At each time step, each robot calculates the reaction and diffusion of its two chemicals and updates itself.

### Reaction Diffusion
At each time step, all of the robots update their chemical concentrations. To do this, we start by having each robot calculate its chemical divergence from its neighbors. This means essentially taking the difference between its own chemical concentrations and the chemical concentrations of its neighbors.

### Robot Movement
Because we want the robots to spatially form interesting shapes, they have to move in a specific way. To start, we must pick a robot that is supposed to move. 
edge robots list to contain any robots that are now on the edge or remove any robots that are no longer on the edge. From this, the robots will scluster around hi If the robot is now neirar a high concentration of B, we signal to look for a new robot in the next time step. If not, we continue to move that same robot. In From thiThis results is n robots clustering around high contcerntrartions of B.2D
.2D

