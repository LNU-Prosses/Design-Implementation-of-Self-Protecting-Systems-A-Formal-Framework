import csv
from sets import Set

with open('ARCS.CSV', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    preqs=dict()
    for row in spamreader:
        if row[0] not  in preqs:
            preqs[row[0]]= []
        preqs[row[0]].append(row[1])

names= dict()
with open('VERTICES.CSV', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        names[row[0]]=row[1]




rulemap=dict()
with open('VERTICES.CSV', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    count=0
    automata = []
    probabilities= []
    ids=dict()
    rule=dict()
    methods=Set()
    methods.add('none')

    for row in spamreader:
        if row[2] !='AND' and row[2] != 'LEAF':
            if not row[1].startswith('canInvoke'):
                automaton=row[1].replace('(','_').replace(',','_').replace(')','')
                if not row[1].startswith('isCompromised'):
                    print automaton+'=Rule('+automaton.upper()+','+str(int(float(row[3])*100))+',none);'
                else:
                    #cut the method part out.
                    method= automaton.split("_")[-1]
                    methods.add(method)
                    print automaton+'=Rule('+automaton.upper()+','+str(int(float(row[3])*100))+','+method+');'
                automata.append(automaton)
                ids[row[0]]=count
                count+=1
                for preq in preqs[row[0]]:
                    #print row[1]+':'+names[preq]
                    rulemap[row[0]]=preq
            else:
                automaton=row[1].replace('(','_').replace(',','_').replace(')','')
                method= automaton.split("_")[-2]
                methods.add(method)
print '\n\n\n'
print ('system call_graph,tactic_tree,'),
for i in range(0,len(automata)):
    if i != len(automata)-1:
        print(automata[i]+','),
    else:
        print(automata[i]+';'),
print '\n\n\nRULES TO DERIVATIONS\n\n\n'
print 'bool prerequisites(const int node){'
for mapping in rulemap:
    #print names[mapping]+':'+names[rulemap[mapping]]+'-->'+str(preqs[rulemap[mapping]])
    prerequisite= 'if(node == '+names[mapping].replace('(','_').replace(',','_').replace(')','').upper()+'){\nreturn '
    prerequisites=[]
    for preq in preqs[rulemap[mapping]]:    
        if preq in ids: 
            prerequisites.append(names[preq].replace('(','_').replace(',','_').replace(')','').upper()+' ')
    if len(prerequisites) > 0:
        for i in range(0,len(prerequisites)):
            if i != len(prerequisites)-1:
                prerequisite+= 'achieved['+prerequisites[i]+'] && '
            else:
                prerequisite+= 'achieved['+prerequisites[i]+'];'
    else:
        prerequisite+=' true;'
            
    print prerequisite+'\n}'
print 'return false;\n}'
                
                    
print '\n\n\n'                
print 'const int N='+str(count)+';'

for i in range(0,len(automata)):
    print 'const int '+automata[i].upper()+' = '+ str(i)+';'

print('bool achieved[N]={'),;
for i in range(0,len(automata)):
    if i != len(automata)-1:
        print('false,'),
    else:
        print('false'),
print '};'
    
               
print 'const int num_methods='+str(len(methods))+';'
count=0
print 'broadcast chan methods[num_methods];'
for m in methods:
    print 'const int '+m+'='+str(count)+';'
    count+=1
print 'bool syn[num_methods]={'
print 'false,'
for i in range( len(methods)-2):
    print 'true,'
print 'true};'
