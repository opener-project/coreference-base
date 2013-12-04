corefgraph
==========

Installation
------------

To install corefgraph and their dependencies as user:

pip install --upgrade --user git+ssh://git@github.com/opener-project/coreference-base.git#egg=corefgraph


Usage 
-----

from $repo/core directory, execute: 

cat input.kaf | python -m corefgraph.process.file --language (de|en|es|fr|it|nl) 


