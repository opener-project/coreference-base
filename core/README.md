Core Installation
-----------------

1. Install pykaf: https://github.com/opener-project/pykaf
2. pip install --upgrade --user networkx 
3. pip install --upgrade --user pyYAML 
4. pip install --upgrade --user lxml 

(optional)

5. In the coreference-base/core directory, execute: 

    sudo python setup.py install 

6. Without sudo rights: 
    
    python setup.py install --prefix=/choose/directory 

In this case *remember* to actually add the above chosen directory to the PYTHONPATH. 

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




