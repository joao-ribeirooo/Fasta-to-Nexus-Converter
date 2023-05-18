# Fasta-to-Nexus-Converter
This repository contains the 2nd homework of the subject, analise de sequencias biologicas, aka ASB 

# What it does?
Well as the name says it will convert any valid fasta file into a nexus file with an addition of a mr bayes block in order to do Bayesian Inference trees. This program reads the fasta file(STDIN) and divides the species names and sequence into a key and value inside of a dictionary, respectively. After it will verify the species names only allowing a maximum of 99 characters. If there is duplicates after truncating them until the 99th character it will add a specific number to them to differentiate. After it will get the values NCHAR, NTAX, NGEN(STDIN), outgroup(STDIN) and a phrase that will be choosen randomly to inspirate everyone that uses this program:D. And after it will use all this values to write a valid nexus file(STDOUT) that can be used for example in mrbayes to create a bayesian inference tree.

# How to use it?
## Linux
Type chmod +x script_name.py in the command prompt
You will write ./filename.py "filename.fasta" "nameofoutgroup" "Numberofgenerations"
Example : ./fastatonexus.py "example.fasta" "Podarcis" "1000000"
## Windows
You will write python filename.py "filename.fasta" "nameofoutgroup" "Numberofgenerations"
Example : python fastatonexus.py "example.fasta" "Podarcis" "1000000"


