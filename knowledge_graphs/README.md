# Knowledge Graph-to-text generation

The component is primarily implemented with [JointGT](https://aclanthology.org/2021.findings-acl.223/).

Examples:

**QUERY**:

    [['Russia', 'capital', 'Moscow']]

**OUTPUT**:
 The capital of Russia is Moscow.

**QUERY**:

    [['Barcelona', 'player', 'Christiano Ronaldo']]

**OUTPUT**:
Christiano Ronaldo is a player in Barcelona.

**QUERY**:

    [['The Big Bang Theory', 'director', 'Mark Cendowski'], 
     ['The Big Bang Theory', 'number of seasons', '12']]

**OUTPUT**:
Mark Cendowski is the director of The Big Bang Theory which has 12 episodes.

**QUERY**:

    [['Moscow Institute of Physics and Technology', 'motto', 'Sapere aude'], 
    ['Moscow Institute of Physics and Technology', 'located in the administrative territorial entity', 'Dolgoprudny']]
**OUTPUT**:
Sapere aude is the motto of Moscow Institute of Physics and Technology which is located in Dolgoprudny.

**QUERY**:

    [['YouTube', 'founded by', 'Steve Chen'], 
    ['YouTube', 'founded by', 'Jawed Karim']]
**OUTPUT**:
Steve Chen and Jawed Karim founded the company, YouTube.
