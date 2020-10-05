#PASS 2 of TWO-PASS ASSEMBLER
#Implement pass-II of a two-pass assembler. The output of assignment-1 (intermediate file, symbol and literal table) should be input for this assignment.
#Global Declarations
LC = 0
PoolIndex = 0

#Initialization
SymTab = {} #Dictionary 
LitTab = {}
PoolTab = []

########  Generate data structur module starts here ########    
def generateDatastructures():
    createSymbTab()
    print (SymTab)
    createLitTab()
    print (LitTab)
    createPoolTab()
    print (PoolTab)
########  Generate data structur module ends here ########    
    
########  Accept Symbol Table starts here ########    
def createSymbTab():
    SymbCnt = int(input("\nEnter total number of Symbols :"))
    for k in range(0, SymbCnt):
        symbol, address = input("Enter Symbol & address - " + str((k+1)) + " : ").split()
        SymTab[symbol] = address    
########  Accept Symbol Table ends here ########


########  Accept Literal Table starts here ########    
def createLitTab():
    LitCnt = int(input("\nEnter total number of Literals :"))
    for k in range(0, LitCnt):
        literal, address = input("Enter Literal & address - " + str((k+1)) + " :").split()
        LitTab[literal] = address    
########  Accept Literal Table ends here ########
        
########  Accept Pool Table starts here ########    
def createPoolTab():
    PoolCnt = int(input("\nEnter total number of pools :"))
    for k in range(0, PoolCnt):
        poolVal =  input("Enter Literal reference for pool " + str(k+1) + ": ")
        PoolTab.append(poolVal)
########  Accept Pool Table ends here ########

######## Process Tok2 starts here ########         
def processTok2(tokens):
    global PoolIndex, LC
    tok1 = tokens[0][:-1]  #Remove last character
    tok2 = tokens[1].rstrip("\n")[:-1]   
    
    if tok1[1:] == "IS":
        TC = str(LC) + ") 00 0 000\n"
        fp2.write(TC)  
    elif ((tok1[1:] == "AD") and (tok2 == "01" or tok2 == "04")): 
	#Only for END and LTORG; No target code for START, ORIGIN, and EQU
        for i in range(int(PoolTab[PoolIndex]), int(PoolTab[PoolIndex+1])):
            literal = list(LitTab)[i]  #access dictionary key’s element by index
            TC = str(LC) + ") 00 0 " + literal + "\n"
            fp2.write(TC)
            LC=LC+1
        #end for
        PoolIndex=PoolIndex + 1 #For next pool processing
        LC = LC-1	#For extra LC increment through for loop
    #End of if-else        
######## Process Tok2 ends here ########        

######## Process Tok4 starts here ########        
def processTok4(tokens): #Eg. (IS,  09)  (S, 0)
    global LC
    tok1 = tokens[0][:-1]  #Remove last character
    tok2 = tokens[1][:-1]
    tok4 = tokens[3].rstrip("\n")[:-1]   
    if tok1[1:] == "AD":
        LC = int(tok4)-1
        TC = "------------\n"
    elif tok1[1:] == "DL":
        if tok2 == "01":  #DS
            TC = ""
            for i in range(0,int(tok4)):
                TC = TC + str(LC) + ")\n" 
                LC = LC + 1
            LC = LC - 1 #After DS
        else: #DC
            TC = str(LC) + ") 00 0 " + tok4 +"\n"
    elif tok1[1:] == "IS":
        Index = list(SymTab)[int(tok4)] #access dictionary key’s element by index
        TC = str(LC) + ") " + tok2 + " 0 " + SymTab[Index] + "\n"
    #End of if-else        
    fp2.write(TC)  
######## Process Tok4 ends here ########         

######## Process Tok5 starts here ########         
def processTok5(tokens):
    tok2 = tokens[1][:-1]  #Remove last character
    tok3 = tokens[2][:-1]
    tok4 = tokens[3][:-1]
    tok5 = tokens[4].rstrip("\n")[:-1]   

    if tok4[1:] == 'S':
        Index = list(SymTab)[int(tok5)]  #access dictionary key’s element by index
        TC = str(LC) + ") " + tok2 + " " + tok3[1:] + " " + SymTab[Index] + "\n"
    elif tok4[1:] == 'L':
        Index = list(LitTab)[int(tok5)]  #access dictionary key’s element by index
        TC = str(LC) + ") " + tok2 + " " + tok3[1:] + " " + LitTab[Index] + "\n"
    #End of if-else        
    fp2.write(TC)  
######## Process Tok5 ends here ########         
 

################## Main program starts here 
generateDatastructures() #Generate Symbol, Literal, and Pool table

fp1 = open("IC.txt","r") # Intermediate code file
fp2 = open("output.txt","w")    # Output target file

for line in fp1:
    tokens = line.split(" ") #Tokenize the instruction
    tokCnt = len(tokens)    #Gives token length

    if tokCnt == 2:
        processTok2(tokens)
    elif tokCnt == 4:
        processTok4(tokens)
    elif tokCnt ==5:  #ADD-DIV, DS/DC, EQU
        processTok5(tokens)
  
    LC=LC+1
######End for ####     

fp1.close()
fp2.close()