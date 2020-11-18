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
