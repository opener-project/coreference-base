[![Build Status](https://drone.io/github.com/opener-project/coreference-base/status.png)](https://drone.io/github.com/opener-project/coreference-base/latest)

# Coreference

This Gem provides coreference resolution for various languages such as English
and Spanish.

The CorefGraph-en module provides an implementation of the Multi-Sieve Pass
system for for Coreference Resolution system originally proposed by the
Stanford NLP Group (Raghunathan et al., 2010; Lee et al., 2011) and (Lee et
al., 2013).  This system proposes a number of deterministic passes, ranging
from high precision to higher recall, each dealing with a different manner in
which coreference manifests itself in running text.

Although more sieves are available, in order to facilitate the integration of
the coreference system for the 6 languages of OpeNER we have included here 4
sieves: Exact String Matching, Precise Constructs, Strict Head Match and
Pronoun Match (the sieve nomenclature follows Lee et al (2013)). Furthermore,
as it has been reported, this sieves are responsible for most of the
performance in the Stanford system.

The implementation is a result of a collaboration between the IXA NLP
(http://ixa.si.ehu.es) and LinguaMedia Groups (http://linguamedia.deusto.es).

## Requirements

* Ruby 1.9.2 or newer
* Python 2.7 or newer
* Pip 1.3.1 or newer

## Installation

Installing as a regular Gem:

    gem install opener-coreference-base

Using Bundler:

    gem 'opener-coreference-base',
      :git    => 'git@github.com:opener-project/coreference-base.git',
      :branch => 'master'

Using specific install:

    gem install specific_install
    gem specific_install opener-coreference-base \
       -l https://github.com/opener-project/coreference-base.git

## Usage

CorefGraph-en requires two inputs (you can see examples in the
resources/examples directory):

1. KAF with wf, terms and entities elements.
2. Constituent syntactic analysis in Treebank format, one sentence per line
   with heads marked.

To run the program execute:

    coreference-base -l (de|en|es|fr|it|nl) -i input.kaf input.treebank

Corefgraph will output KAF via standard output with the <coreference> clusters
added to the KAF input received. Note that for the full functionality of
CorefGraph you will need to provide the treebank input with the heads of (at
least) the Noun Phrases marked, as it can be seen in the treebank input
examples in the resource/examples directory. If you do not provide heads, only
Exact String Match will work properly, whereas Precise Constructs, Strict Head
Match and Pronoun Match will not.

For a full explanation of how the Multi Sieve Pass system works see
documentation in resources/doc.

# Adapting CorefGraph-en to your language

There are a number of changes needed to be made to make CorefGraph works for
other languages. Although we have try to keep the language dependent features
to a minimum, you will still need to create some dictionaries for your own
language and make some very minor changes in the code. Here is the list of very
file in the Corefgraph module that needs to be changed.  Every change except
one (see below) to be done in the **$project/resources** directory:

* dictionaries/$lang\_determiners.py
* dictionaries/$lang\_pronouns.py
* dictionaries/$lang\_verbs.py
* dictionaries/$lang\_stopwords.py

* tagset/$TAGSETNAME\_pos.py
* tagset/$TAGSETNAME\_constituent.py
* tagset/$TAGSETNAME\_ner.py

* files/animate/$lang.animate.txt
* files/animate/$lang.inanimate.txt

* files/demonym/$lang.txt

* files/gender/$lang.male.unigrams.txt
* files/gender/$lang.female.unigrams.txt
* files/gender/$lang.neutral.unigrams.txt
* files/gender/$lang.namegender.combine.txt
* files/gender/$lang.gender.data

* files/number/$lang.plural.unigrams.txt
* files/number/$lang.singular.unigrams.txt

**IMPORTANT!!!** In the top module directory, you will need to modify
**properties.py** according to the names of the files you generated above for
your own language.

## Python Structure

The contents of the CorefGraph module are the following:

* core/features: Gender and Number feature extraction of pronouns
* core/graph: Graph utils for traversal of Syntactic Trees. Used for Antecedent
  Selection mainly.
* core/multisieve: Implemented Sieve passes plus several dictionaries.
* core/output: Various output utilities
* core/process.py: Main module. Use this to execute the system.
* core/pykaf: KAF output utilities
* core/resources: Most dictionaries (gender, number, animacy, demonyms) are
  placed here.
* core/test: Testing funcionalities
