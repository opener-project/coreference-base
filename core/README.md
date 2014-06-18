Core Installation
-----------------

1. pip install --upgrade --user hg+https://bitbucket.org/Josu/pykaf#egg=pykaf
2. pip install --upgrade --user networkx 

(optional if logging is wanted)

3. pip install --upgrade --user pyYAML 

Core Usage 
----------

For coreference resolution, execute, from core/ directory: 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) 

for singleton clusters (automatic markables in annotation jargon): 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) --singleton --sieves NO

for drone.io testing: 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) --time_stamp now 

if unsure that the constituent parsing KAF layer is well-formattted: 

   cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) --unsafe_tree

for help: 

    python -m corefgraph.process.file --help




