Core Installation
-----------------

1. pip install --upgrade --user git+ssh://git@github.com/opener-project/pykaf.git
2. pip install --upgrade --user networkx 
3. pip install --upgrade --user pyYAML 

Core Usage 
----------

If you did not do 5. or 6. above, from $repo/core directory, execute: 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) 

for singleton clusters (automatic markables in annotation jargon): 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) --singleton 

for drone.io testing: 

    cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) --time_stamp now 

for help: 

    python -m corefgraph.process.file --help




