Core Usage 
----------

from $repo/core directory, execute: 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) 

for singleton clusters (automatic markables in annotation jargon): 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) --singleton 

for drone.io testing: 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) --time_stamp now 

for help: 

    python -m corefgraph.process.file --help




