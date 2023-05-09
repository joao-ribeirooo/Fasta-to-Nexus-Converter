import sys
import random


def ReadFile(filename):
    '''
    Reads the fasta file and inserts into a dictionary the species name and the sequence, respectively
    Input: Fasta File
    Output: Dicionario que contem o nome da especie e a respetiva sequencia
    '''
    fastahandle = open(filename, "r")
    Dicionario = {}
    for row in fastahandle:
        if row.startswith(">"):
            name = row.strip()
            name = name[:99]
            Dicionario[name] = ""
        else:
            Dicionario[name] += row.strip()       
    fastahandle.close()
    return Dicionario

def VariableNTAX(Dicionario):
    ntax = len(Dicionario)
    return ntax

def VariableNCHAR(Dicionario):
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
    outgroup = ">" + outgroup
    outgroup = outgroup[:99]
    if outgroup not in Dicionario.keys():
        print("The outgroup doesnt seem to be one of the species names inside the fasta file")
        exit()
    else:
        outgroup = outgroup.replace(">", "")   
    return outgroup

def VariableNgen(ngen):
    return ngen

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


def WriteFileNexus(nchar, ntax, outgroup, ngen, fraseinspiradora,  Dicionario):
    print(f"""[{fraseinspiradora}]
#NEXUS

BEGIN DATA;
DIMENSIONS NTAX={ntax} NCHAR={nchar};
FORMAT DATATYPE=DNA MISSING=N GAP=-;
MATRIX""")
    for SpeciesName, sequence in Dicionario.items():
        SpeciesName = SpeciesName.replace('>', '')
        print('    '+ SpeciesName + '  ' + sequence)
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
    nchar = (VariableNCHAR(Dicionario))
    ntax = (VariableNTAX(Dicionario))
    outgroup = VariableOutgroup(Dicionario, sys.argv[2])
    ngen = VariableNgen(sys.argv[3])
    fraseinspiradora= FraseInspiradora()
    WriteFileNexus(nchar,ntax, outgroup, ngen, fraseinspiradora, Dicionario)