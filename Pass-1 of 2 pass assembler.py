#PASS 1 of TWO-PASS ASSEMBLER
#Design suitable data structures and implement pass-I of a two-pass assembler. Implementation should consist of a few instructions from each category and few assembler directives.

#Global Declarations
LC = 0
PoolCnt = 0
LitCnt = 0

#Initialization
OPTAB =["STOP","ADD","SUB","MULT","MOVER","MOVEM","COMP","BC","DIV","READ","PRINT"]
REGTAB = ["AREG","BREG","CREG"]
CONDTAB = ["LT","LE","EQ","GT","GE","ANY"]
ADTAB = ["START","END","ORIGIN","EQU","LTORG"]

SymTab = {} #Dictionary 
LitTab = {}
PoolTab = [0]


def searchOp(Tok): # Function prototype
    for i in range(len(OPTAB)):  #ITERATE THROUGH RANGE OF INDICES
        if Tok == OPTAB[i]:    
            return i  #successful search with the index       
    return -1         #unsuccessful search

def searchDirective(Tok):
    for i in range(len(ADTAB)):  #ITERATE THROUGH RANGE OF INDICES
        if Tok == ADTAB[i]:    
            return i               
    return -1       

def searchSymb(Tok):
    if Tok in SymTab:
        return list(SymTab.keys()).index(Tok)
    else:   
        return -1

def searchLit(Tok):
    global PoolCnt, LitCnt
    for k in range(PoolTab[PoolCnt], LitCnt):
        if ( list(LitTab)[k] == Tok ):
            return k
    return -1

def searchCond(Tok):
    if Tok in CONDTAB:
        return CONDTAB.index(Tok)
    else:   
        return -1

def searchReg(Tok):
    if Tok in REGTAB:
        return REGTAB.index(Tok)
    else:   
        return -1    
    
########  Process 1 token case starts here ########   
def processTok1(Tok):
    global LC, PoolCnt, LitCnt
    Tok = Tok.rstrip("\n")
    
    #Process Imperative Statement
    i = searchOp(Tok) 
    if ( i == 0): #STOP 
        IC = "(IS, "+ str('%02d' % i) + ") \n"
    else:
         #Process Assembler Directive
        i = searchDirective(Tok)
        IC = "(AD, "+ str('%02d' % i) + ") \n"
        if (i == 0): LC = LC - 1
        if (i == 1 or i == 4): #END or LTORG
            for k in range(PoolTab[PoolCnt], LitCnt):
                LitTab[list(LitTab)[k]] = LC
                LC=LC+1

            PoolCnt = PoolCnt+1
            LC = LC - 1
            PoolTab.append(LitCnt)
   
    fp2.write(IC)       
########  Process 1 token case ends here ########


########  Process 2 tokens case starts here ########    
def processTok2(tokens):
    global LC
    Tok1 = tokens[0]
    Tok2 = tokens[1].rstrip("\n")
    
    #Process Imperative Statement
    i = searchOp(Tok1) 
    if ( i == 9 or i == 10): # READ or PRINT
        j = searchSymb(Tok2)
        if (j == -1 ):
            SymTab[Tok2]="-1" #Tok2:-1
        
        symIndex = list(SymTab.keys()).index(Tok2)
        IC = "(IS, "+ str('%02d' % i) + ") (S, " + str(symIndex) + ")\n"
        fp2.write(IC)               
    #Process Assembler Directive
    i = searchDirective(Tok1)
    if ( i == 0 or i == 2): # START or ORIGIN
        LC = int(Tok2)-1
        IC = "(AD, "+ str('%02d' % i) + ") (C, " + Tok2+ ")\n"
        fp2.write(IC)
########  Process 2 tokens case ends here ########

######## Process IS for 3 tokens starts here  ########    
def processIS(Tok1, Tok2, Tok3):
    global LitCnt
    flag=0
    #Process Imperative Statement
    i = searchOp(Tok1) 
    if ( i >= 1 and i <= 8): # ADD TO DIV
        flag = 1
        if (Tok3[0] == '=' ): #Operand is a LITERAL
            j = searchLit(Tok3)
            if ( j == -1 ):
                LitTab[Tok3] = "-1" 
                LitCnt = LitCnt + 1
            litIndex = list(LitTab.keys()).index(Tok3)
            Tok3IC = "(L, " + str(litIndex) + ")"
        else:  #Operand is a Symbol
            j = searchSymb(Tok3)
            if (j == -1 ):
                SymTab[Tok3]="-1" #Tok3 with address = -1
            symIndex = list(SymTab.keys()).index(Tok3)
            Tok3IC = "(S, " + str(symIndex) + ")"
       
        regIndex = searchCond(Tok2) if (i == 7 ) else searchReg(Tok2) #i == 7 means BC
        
        IC = "(IS, "+ str('%02d' % i) + ") (" + str(regIndex) +") " + Tok3IC + "\n"
        fp2.write(IC)   
        return flag            
########  Process IS for 3 tokens ends here ########


######## Process DL for 3 tokens starts here  ########    
def processDL(Tok1, Tok2, Tok3):
    global LC
    flag = 0
    
    #Process Declarative Statement
    if ( Tok2 == "DC" or Tok2 == "DS" ):
        flag = 1     
        SymTab[Tok1] = LC #Tok3 with address = LC
                
        if (Tok2 == "DS"): 
            LC = LC + int(Tok3) -1
            IC = "(DL, 00) (C, "+ Tok3 + ")\n"  #for DS
        else:
            IC = "(DL, 01) (C, "+ Tok3 + ")\n"  #for DC
        fp2.write(IC)   
        return flag            
########  Process DL for 3 tokens ends here ########

######## Process EQU for 3 tokens starts here  ########    
def processEQU(Tok1, Tok2, Tok3):
    global LC
   
    #Process EQU Statement
    i = searchDirective(Tok2)
    if ( i == 3): # EQU
        LC = LC-1
        SymTab[Tok1] = SymTab[Tok3]
        IC = "(AD, "+ str('%02d' % i) + ") \n"
        fp2.write(IC)
    
########  Process EQU for 3 tokens ends here ########

################## Main program starts here 
fp1 = open("input.asm","r") # ASM file
fp2 = open("IC.txt","w")    # IC file

for line in fp1:
    tokens = line.split(" ") #Tokenize the instruction
    tokCnt = len(tokens)    #Gives token length

    if tokCnt == 1:
        processTok1(tokens[0])
    elif tokCnt == 2:
        processTok2(tokens) #user-defined functions
    elif tokCnt ==3:  #ADD-DIV, DS/DC, EQU
        Tok1 = tokens[0]
        Tok2 = tokens[1]
        Tok3 = tokens[2].rstrip("\n")
        
        if (processIS(Tok1, Tok2, Tok3)): pass
        if (processDL(Tok1, Tok2, Tok3)): pass
        processEQU(Tok1, Tok2, Tok3)
    elif tokCnt == 4:
        Tok1 = tokens[0]
        Tok2 = tokens[1]
        Tok3 = tokens[2]
        Tok4 = tokens[3].rstrip("\n")
        SymTab[Tok1] = LC
        processIS(Tok2, Tok3, Tok4) 
    LC=LC+1
######End for ####     
print ("\nSymbol Table:")
print(SymTab)
print ("\nLiteral Table:")
print (LitTab)
print ("\nPool Table:")
print (PoolTab)

fp1.close()
fp2.close()
    
    
