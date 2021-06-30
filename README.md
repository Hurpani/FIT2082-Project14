# Application of Network Metrics for Simulation Validation - Camponotus fellah ant social networks case study
## Originally FIT2082-Project14 in semester 2 of 2020.

## Summary
In this study, we sought to examine the application of network metrics for simulation validation.
Using the example of ant social networks, and the study by Mersch et al. (2013) for our real-world
data, we designed a simple simulation of ant behaviours using some basic assumptions age polyethism.
This yields example simulation networks against which we can compare network metrics associated with
real-world data, and metrics associated with social networks of randomised social interactions.

This repository contains the source code for our software agent-based simulation model. There are
some implementation details pertaining to the behaviour of the ants which benefit from elaboration
beyond what we provide in our write-up; I explore these below.

In our experiment, ants are modelled as individual actors or agents in a grid, where they move
by making choices of adjacent, free tiles. Their choices are not uniformly random, but biased by
a series of factors which tend to shift as a function of the ant's age and its surroundings. The
selection of these functions is intended to follow the rough age castes as observed in the results
in the experiment due to Mersch et al. (2013), so as to implement the hypothesis that an ant's age
influences its tendencies towards (physical) locations, and through this, its role in the colony.

* * * * *

## Technical Details: Bias Factors
At each tick, there is 20 per cent chance that an ant will remain still. Otherwise, it picks one of
eight adjacent tiles (via the eight cardinal/intercardinal directions) at random, with each choice
being weighted and higher weights making such a choice more likely. Initially, all weights are either
0 or 1; 0 if the location is obstructed, and 1 otherwise.

Each ant knows its current direction, and it has a tendency (by default, via a factor of h=10) to prefer
a similar direction to its current direction of motion. If a particular direction is represented as a
linear combination of canonical basis vectors in 2D Euclidean space, where the coefficients can only be
-1, 0, or 1, then the reciprocal of 1 plus the L2 norm of the difference between the current direction
and a given direction gives a bias factor. The product of this bias, the h-value, and the current
weighting, gives the new weighting for each direction.

Additionally as a function of the ant's age, for each free location, a small bias is added depending on
the pheromone type and count of that location. These pheromones are either "generic" or "brood" pheromones,
and they are preferred more or less depending on how old an ant is - once again, mimicing the age
polyethism hypothesis.

Finally, there are some bias factors which drive foraging behaviour. Ants will tend towards locations which
contain food, and as they grow older, will have the weighting of pheromone-free locations bolstered. These
ants also leave behind "foraging" pheromones, and will seek these ones out. Altogether, these rules form
a simple system which governs the behaviour of the agents/"ants" in the simulation model.

* * * * *

## References

Mersch, D., Crespi, A., Keller, L. (2013). _Tracking Individuals Shows Spatial Fidelity Is a KeyRegulator of
Ant Social Organization_. Science, 340(6136), 1090-1093.
www.jstor.org/stable/41985413
