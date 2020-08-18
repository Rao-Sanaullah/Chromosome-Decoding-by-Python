##=======================================================================
# Packages
##=======================================================================
from random import randint
from random import randrange
from copy import deepcopy


##=======================================================================
# Parameters
##=======================================================================
G = [0,0,1,1,2,3,2,5,4,0,6,3,1,7,6,2,5,6,8]
nf = ['AND','NOT','OR']
ni = 3
no = 2
nr = 3
nc = 3
a = 2                           # Arity
l = nc                          #levels-back
nn = a + 1                      #size of each node 
Ln = nc * nr                    #No of Nodes
Lg = (nc * nr * (a + 1)) + no   #Total no of elemet in a chromosome 
M = Ln + ni                     #Max. Addresses in a Graph


##=======================================================================
# Methods
##=======================================================================
def printls(ls):
    for item in ls:
        print(item)


def NodesToProcess():
    def Arity(F):
        if F == "NOT":
            return(1)
        else:
            return(2)

    NU = [False]*M

    for i in range(Lg-no,Lg):
        NU[G[i]] = True

    # Find active nodes
    NG = [None]*nn
    for k in range(Ln): # Iterate over all nodes
        for i in range(ni,M):
            if NU[i] == True:
                index = nn*(i-ni)
                for j in range (0, nn):
                    NG[j] = G[index+j] # Get node genes
                for j in range (1, Arity(nf[NG[nn-3]])+1):
                    NU[NG[j]] = True
    
    NP = []
    for j in range (ni, M):
        if NU[j] == True:
            NP.append(j)

    dic_nodes = {}  #Dictionary Initialize 
    for j in range(0,len(NP)):
        node = []
        g = nn * (NP[j]-ni) # Function gene
        node.append(G[g])

        for i in range(1,nn):
            node.append(G[g+i]) # Connection gene

        dic_nodes[NP[j]] = node # Dictionary

    return(dic_nodes)


def decode():
    nodes = NodesToProcess()
    decoded = []

    for i in range (ni):  #Inputs
        decoded.append("Input({})".format(i))

    for item in G[Lg-no:]:
        decoded.append("Output({})".format(item))  #Outputs

    for key, value in nodes.items(): 
        func = nf[value[0]]
        if func == 'NOT':
            decoded.append("{} = {}({})".format(key,func,value[1]))
        else:
            decoded.append("{} = {}({}, {})".format(key,func,value[1],value[2]))

    return(decoded)


def random_sol():
    G = []
    for j in range(nc):
        for k in range(nr):
            # function bit
            bit0 = randint(0,len(nf)-1)
            # connection bit 1
            if j>=l:
                bit1 = randint(ni+(j-l)*nr, ni+j*nr-1)
            else:
                bit1 = randint(0, ni+j*nr-1)
            # connection bit 2
            if j>=l:
                bit2 = randint(ni+(j-l)*nr, ni+j*nr-1)
            else:
                bit2 = randint(0, ni+j*nr-1)

            # appending to chromosome
            G.append(bit0)
            G.append(bit1)
            G.append(bit2)

    for k in range(no):
        # output bit
        G.append(randint(ni, ni+Ln-1))
    
    return(G)


def random_walker(G,h):

    for k in range(h):
        # generate a random index in range length(chromosome) or Lg
        i_bit = randrange(Lg)

        if i_bit >= (Lg-no):  # its an output bit
            while (True):
                to_replace = randint(ni, ni+Ln-1)
                if not(G[i_bit] == to_replace):
                    G[i_bit] = to_replace
                    break

        elif i_bit % 3 == 0 or i_bit == '0': # its a function bit
            while (True):
                to_replace = randint(0,len(nf)-1)
                if not(G[i_bit] == to_replace):
                    G[i_bit] = to_replace
                    break

        else: # else its a connection bit
            for index in range(nc):
                if i_bit in range(nr*nn*index, (nr*nn*(index+1))):
                    j = index

            if j>=l:
                while (True):
                    to_replace = randint(ni+(j-l)*nr, ni+j*nr-1)
                    if not(G[i_bit] == to_replace):
                        G[i_bit] = to_replace
                        break
            else:
                while (True):
                    to_replace = randint(0, ni+j*nr-1)
                    if not(G[i_bit] == to_replace):
                        G[i_bit] = to_replace
                        break

    return (G)


##=======================================================================
# Main
#=======================================================================

G = random_sol()
print(G)

netlist = decode()
printls(netlist)

G = random_walker(deepcopy(G), 3)
print(G)


