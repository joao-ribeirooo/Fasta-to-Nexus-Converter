import sys
import random
from collections import Counter

def ReadFile(filename):
    '''
    Reads the fasta file and inserts into a Dicionario the species name and the sequence, respectively
    Input: Fasta File
    Output: Dicionario que contem o nome da especie e a respetiva sequencia >IGRA5
    '''
    fastahandle = open(filename, "r")
    Dicionario = {}
    for row in fastahandle:
        if row.startswith(">"):
            name = row.strip()
            name = name.replace(">", "")
            name = name.replace(" ", "_")
            Dicionario[name] = ""
        else:
            Dicionario[name] += row.strip() 
    fastahandle.close()
    return Dicionario

def VerifyNames(Dicionario):
    """
    If there is a name in the dictionary with 99 or more characters it cuts out the one with more than 99 characters and the rest stays the same. 
    If there are two or more names with 99 characters or more it checks for duplicates.
    If there are duplicates it will cut them down to character 95 and add a number to differentiate between them.
    Input : Dictionary 
    Output : Dictionary with the replacement of the duplicate keys and with more than 99 characters
    """
    #longkey = {x for x in Dicionario.keys() if len(x) >= 99}
    longkey = {}   
    for key in Dicionario.keys():
        if len(key) >= 99:
            longkey[key] = key[:99]
    Dup = (Counter(longkey.values()) - Counter(set(longkey.values()))).keys()
    counter = 0    
    for key, name in longkey.items():
        if name in Dup:
            counter += 1
            newkey = name[:95] + str("%04d" % (counter,))
            Dicionario[newkey] = Dicionario.pop(key)
        else:
            newkey = name[:99]
            Dicionario[newkey] = Dicionario.pop(key)
    return Dicionario

def VariableNCHAR(Dicionario):
    """
    It will get the NCHAR value by looping through the dictionary
    """
    lenghts = set()
    for SpeciesName, sequence in Dicionario.items():
        lenghts.add(len(sequence))
    if len(lenghts) == 1:
        nchar = len(sequence)
    else:
        print("The sequences do not have the same character lenght")
        exit()
    return nchar

def VariableOutgroup(Dicionario, outgroup):
    outgroup = outgroup.replace(" ", "_") #in case there is spaces to match the specie name inside the dictionary
    outgroup = outgroup.replace(">", "") #in case there is > to match the specie name inside the dictionary
    outgroup = outgroup[:99]
    if outgroup not in Dicionario.keys():
        print("The outgroup doesnt seem to be one of the species names inside the fasta file")
        exit()
    else:
        return outgroup

def FraseInspiradora():
    FraseRand = ["When there is a true desire in the heart, and that desire is strong, that is when he finds real strength that even he did not know he had!",
    "Hurt me with the truth. But never comfort me with a lie.", 
    "Peoples lives dont end when they die, it ends when they lose faith.",
    "Theres no shame in falling down! True shame is to not stand up again!",
    "I do not fear this new challenge, rather like a true warrior I will rise to meet it.",
    "Once You're In The Darkness, You Just Sink Deeper Into It. Keep Your Light Shining.",
    "Everyone Is Burdened With Their Sins. They'll Never Go Away. Even So, We Still Carry On With What We Must Do.",
    "No matter how messed up things get, you can always figure out the best solution.",
    "Believe in your own power.",
    "Sometimes the things that matter the most are right in front of you."
    ]
    fraseinspiradora = random.choice(FraseRand)
    return fraseinspiradora

def WriteFileNexus(nchar, outgroup, ngen, fraseinspiradora,  Dicionario):
    print(f"""[{fraseinspiradora}]
#NEXUS

BEGIN DATA;
DIMENSIONS NTAX={len(Dicionario)} NCHAR={nchar};
FORMAT DATATYPE=DNA MISSING=N GAP=-;
MATRIX""")
    for SpeciesName, sequence in Dicionario.items():
        #print('    '+ SpeciesName + '  ' + sequence)
        print("{: >99} ".format(SpeciesName) + '  ' + sequence)

    print("  ;" + "\n" + "  end;")
    print(f'''
begin mrbayes;
set autoclose=yes;
outgroup={outgroup};
mcmcp ngen={ngen} printfreq=1000 samplefreq=100 diagnfreq=1000 nchains=4 savebrlens=yes filename=MyTree01;
mcmc;
sumt filename=MyTree01;
end;''')
    
if __name__ == "__main__":
    Dicionario = ReadFile(sys.argv[1])
    Dicionario2 = VerifyNames(Dicionario)
    nchar = (VariableNCHAR(Dicionario2))
    outgroup = VariableOutgroup(Dicionario2, sys.argv[2])
    fraseinspiradora= FraseInspiradora()
    WriteFileNexus(nchar, outgroup, sys.argv[3], fraseinspiradora, Dicionario2)
