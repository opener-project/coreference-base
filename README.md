
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

The implementation is a result of a collaboration between the IXA NLP (ixa.si.ehu.es) and
LinguaMedia Groups (http://linguamedia.deusto.es).

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
    +

- README.md: This README


INSTALLATION
============

Installing the ixa-opennlp-tok-en requires the following steps:

If you already have installed in your machine JDK6 and MAVEN 3, please go to step 3
directly. Otherwise, follow these steps:

1. Install JDK 1.6
-------------------

If you do not install JDK 1.6 in a default location, you will probably need to configure the PATH in .bashrc or .bash_profile:

````shell
export JAVA_HOME=/yourpath/local/java6
export PATH=${JAVA_HOME}/bin:${PATH}
````

If you use tcsh you will need to specify it in your .login as follows:

````shell
setenv JAVA_HOME /usr/java/java16
setenv PATH ${JAVA_HOME}/bin:${PATH}
````

If you re-login into your shell and run the command

````shell
java -version
````

You should now see that your jdk is 1.6

2. Install MAVEN 3
------------------

Download MAVEN 3 from

````shell
wget http://www.apache.org/dyn/closer.cgi/maven/maven-3/3.0.4/binaries/apache-maven-3.0.4-bin.tar.gz
````

Now you need to configure the PATH. For Bash Shell:

````shell
export MAVEN_HOME=/home/ragerri/local/apache-maven-3.0.4
export PATH=${MAVEN_HOME}/bin:${PATH}
````

For tcsh shell:

````shell
setenv MAVEN3_HOME ~/local/apache-maven-3.0.4
setenv PATH ${MAVEN3}/bin:{PATH}
````

If you re-login into your shell and run the command

````shell
mvn -version
````

You should see reference to the MAVEN version you have just installed plus the JDK 6 that is using.

3. Get module from bitbucket
-------------------------

````shell
hg clone ssh://hg@bitbucket.org/ragerri/ixa-opennlp-tok-en
````

4. Move into main directory
---------------------------

````shell
cd ixa-opennlp-tok-en
````

5. Install module using maven
-----------------------------

````shell
mvn clean install
````

This step will create a directory called target/ which contains various directories and files.
Most importantly, there you will find the module executable:

ixa-opennlp-tok-en-1.0.jar

This executable contains every dependency the module needs, so it is completely portable as long
as you have a JVM 1.6 installed.

The program accepts standard input and outputs tokenized text in KAF.

To run the program execute:

````shell
cat file.txt | java -jar $PATH/target/ixa-opennlp-tok-en-1.0.jar
````

GENERATING JAVADOC
==================

You can also generate the javadoc of the module by executing:

````shell
mvn javadoc:jar
````

Which will create a jar file core/target/ixa-opennlp-tok-en-1.0-javadoc.jar


Contact information
===================

````shell
Rodrigo Agerri
IXA NLP Group
University of the Basque Country (UPV/EHU)
E-20018 Donostia-San Sebastián
rodrigo.agerri@ehu.es
````
