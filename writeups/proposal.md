# Project Proposal
*Nathan Estill, Jonathan Zerez*

## Introduction
At the highest level, the point of our project is the simulate and model decentralized swarms of relatively simple agents in order to build an understanding of how tweaking and tuning local interaction rules impacts the aggregate emergent behavior of the swarm.

## Motivation
We are interested in this project for a number of reasons. Firstly, emergent behaviors are really interesting to study. We find it really cool how simple agents that follow simple rules can collectively perform really complex behaviors. Beyond purely academic interest, we are investigating decentralized swarms as they many potential real world applications. Decentralized swarms are really easily scalable and are very robust to changes in the local environment. Additionally, they are very robust to damages or losses that may occur to any individual agent.

From a more academic point of view, understanding how local interactions impact emergent behavior has many implications for society. For instance in biology, cells can only interact with their direct neighbors, but still are able to form complex structures like tissues and organs. Understanding emergent behavior helps to better understand other complex systems in nature.

From a practical point of view, there are a few societal implications:
* Because decentralized swarms are robust to agent damage or losses, swarms could be well suited for dangerous environments that are too unpredictable for humans or conventional robots.
* Decentralized swarming is something that is not yet fully developed and applied in industry, but it does have the potential to displace additional jobs, as decentralized robot swarms automate away tasks that are currently done by humans and can't be automated using traditional robots.

## Topics
We're currently unsure about what specifically we want to cover beyond decentralized swarms. However, we are pretty sure that we are going to start by replicating a research paper that interests us, and then create an extension of that paper. This will be our MVP. Our stretch goal is to do some work on building a parameterization of how input variables impact the final emergent behavior of the swarm.

## Timeline
* **Week 1:** Start initial research (ie: reading papers/texts) about swarming and identify projects/problems to replicate. We will plan to start with rudimentary simulations in python and visualize with `matplotlib`.
* **Week 2:** Create first pass replication of our identified project/problem. Decide on possible extension to the project/problem (ex: adding functionalities, performing parameter sweeps to characterize the problem, etc).
* **Week 3:** Finish up project extension. Start researching how to model swarms in ROS/Gazebo or other physics based simulations.
* **Week 4:** Implement project in physics based simulator
* **Week 5:** Code cleanup and documentation

## Risks
This is a new area for both of us, so there are a number of risks:
* Swarms require a lot of agents so if we are not careful about efficiency, simulations could take a long time to run
* Finding a paper that is easily replicatable and has clear enough results to validate our work could be difficult
* Integrating a swarm model into a physics based simulator could be challenging and increase run time
* Understanding how to describe emergent behavior in quantitative ways in order to parameterize it
* General validation, ensuring that our model is working how we would expect
