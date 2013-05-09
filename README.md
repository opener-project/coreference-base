# Opener::Kernel::EHU::Coreference::EN

EHU-Coreference_EN_kernel
=========================

The CorefGraph-en module provides an implementation of the Multi-Sieve Pass system for
for Coreference Resolution system originally proposed by the Stanford NLP
Group (Raghunathan et al., 2010; Lee et al., 2011) and (Lee et al., 2013).
This system proposes a number of deterministic passes, ranging from high precision to
higher recall, each dealing with a different manner in which coreference
manifests itself in running text.

Although more sieves are available, in order to facilitate the integration of
the coreference system for the 6 languages of OpeNER we have included here 4 sieves:
Exact String Matching, Precise Constructs, Strict Head Match and Pronoun Match (the
sieve nomenclature follows Lee et al (2013)). Furthermore, as it has been reported,
this sieves are responsible for most of the performance in the Stanford system.

The implementation is a result of a collaboration between the IXA NLP (http://ixa.si.ehu.es) and
LinguaMedia Groups (http://linguamedia.deusto.es).


## Installation

Add this line to your application's Gemfile:

    gem 'EHU-coreference_EN_kernel', :git=>"git@github.com/opener-project/EHU-coreference_EN_kernel.git"

And then execute:

    $ bundle install

Or install it yourself as:

    $ gem specific_install EHU-coreference_EN_kernel -l https://github.com/opener-project/EHU-coreference_EN_kernel.git


If you dont have specific_install already:

    $ gem install specific_install

## Usage

Once installed as a gem you can access the gem from anywhere:


TODO: Change output below as needed
````shell
echo "foo" | EHU-coreference_EN_kernel
````

Will output

````
oof
````

## Contributing

1. Pull it
2. Create your feature branch (`git checkout -b features/my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin features/my-new-feature`)
5. If you're confident, merge your changes into master.

Contents
========

The contents of the CorefGraph module are the following:

    + features/	    Gender and Number feature extraction of pronouns
    + graph/	    Graph utils for traversal of Syntactic Trees. Used for Antecedent Selection mainly.
    + multisieve/   Implemented Sieve passes plus several dictionaries.
    + output/	    Various output utilities
    + process.py    Main module. Use this to execute the system.
    + pykaf/	    KAF output utilities
    + resources/    Most dictionaries (gender, number, animacy, demonyms) are placed here.
    + test/	    Testing funcionalities

- README.md: This README


INSTALLATION
============

In order to run CorefGraph coreference module you need to install the python graph library
graph-tool; please install at least version 2.2.20:

http://projects.skewed.de/graph-tool/


If you run a Debian based linux system such as Ubuntu or Linux Mint, you can easily install
graph-tool and all its dependencies by apt-get the packages built by the graph-tool developer.

If you run a Red Hat based server you can try to use alien to generate .rpm packages from the .deb
ones or you can try and compile from source (good luck).

USING CorefGraph-en
===================

CorefGraph-en requires two inputs (you can see examples in the resources/examples directory):

1. KAF with wf, terms and entities elements.
2. Constituent syntactic analysis in Treebank format, one sentence per line with heads marked.

To run the program execute:

````shell
python process.py -i input.kaf input.treebank
````

CorefGraph-en will output KAF via standard output with the <coreference> clusters added to the KAF input received. Note
that for the full functionality of CorefGraph you will need to provide the treebank input with the heads of (at least) the
Noun Phrases marked, as it can be seen in the treebank input examples in the resource/examples directory. If you do not provide
heads, only Exact String Match will work properly, whereas Precise Constructs, Strict Head Match and Pronoun Match will not.

For a full explanation of how the Multi Sieve Pass system works see documentation in resources/doc.

ADAPTING CorefGraph-en to your language
=======================================

There are a number of changes needed to be made to make CorefGraph works for other languages. Although we have try to
keep the language dependent features to a minimum, you will still need to create some dictionaries for your own language
and make some very minor changes in the code. Here is the list of very file in the Corefgraph module that needs to be changed.
Every change except one (see below) to be done in the $project/resources directory:

    + dictionaries/$lang_determiners.py
    + dictionaries/$lang_pronouns.py
    + dictionaries/$lang_verbs.py
    + dictionaries/$lang_stopwords.py

    + tagset/$TAGSETNAME_pos.py
    + tagset/$TAGSETNAME_constituent.py
    + tagset/$TAGSETNAME_ner.py

    + files/animate/$lang.animate.txt
    + files/animate/$lang.inanimate.txt

    + files/demonym/$lang.txt

    + files/gender/$lang.male.unigrams.txt
    + files/gender/$lang.female.unigrams.txt
    + files/gender/$lang.neutral.unigrams.txt
    + files/gender/$lang.namegender.combine.txt
    + files/gender/$lang.gender.data

    + files/number/$lang.plural.unigrams.txt
    + files/number/$lang.singular.unigrams.txt

**IMPORTANT!!!** In the top module directory, you will need to modify properties.py according to the names of the files
you generated above for your own language.

Contact Information
===================

````shell
Rodrigo Agerri
IXA NLP Group
University of the Basque Country (UPV/EHU)
E-20018 Donostia-San Sebastian
rodrigo.agerri@ehu.es
````
