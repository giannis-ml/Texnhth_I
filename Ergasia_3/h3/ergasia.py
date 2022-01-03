from datetime import date
import pandas as pd
import random
import csp
import math


def constraints_function(A, a, B, b):
    if(myDict[A][0]==myDict[B][0] and (a-b>=3 or b-a>=3)):
        return True
    if(myDict[A][1]==myDict[B][1] and (a-b>=3 or b-a>=3)):
        return True
    if((A==B+"_lab" and a==b+1)or (B==A+"_lab" and b==a+1)):
        return True
    if((myDict[A][3]==True and (b>=a+2 or b<a))or(myDict[B][3]==True and (a>=b+2 or a<b))):
        return True
    if((myDict[A][2]==True and myDict[B][2]==True)and(b-a>=2 or a-b>=2)):
        return True
    return False

def display_program(assignment):
    for i in assignment:
        if(assignment[i]%3==0):
            time="9-12"
        elif(assignment[i]%3==1):
            time="12-3"
        else:
            time="3-6"
        print (i," Mέρα εξέτασης:",math.ceil((assignment[i]+1)/3),"Ώρα εξέτασης: ",time)
        
        

def minimum_remaining_value_sorting(variables,domains):
    min=len(domains[variables[0]])
    index=-1
    for i in range(len(domains)):
        if(len(domains[variables[i]])<min):
            min=len(domains[variables[i]])
            index=i
    return i

df= pd.read_csv('Στοιχεία Μαθημάτων.csv')
semesters= df['Εξάμηνο']
courses= df['Μάθημα']
professors= df['Καθηγητής']
difficultly= df['Δύσκολο (TRUE/FALSE)']
labs= df['Εργαστήριο (TRUE/FALSE)']
myDict={}
for i in range(len(courses)):
    myDict[courses[i]]=[]
for i in range(len(courses)):
    myDict[courses[i]].append(semesters[i])
    myDict[courses[i]].append(professors[i])
    myDict[courses[i]].append(difficultly[i])
    myDict[courses[i]].append(labs[i])
temp=[]
for i in range(len(courses)):
    temp.append(courses[i])
for i in range(len(courses)):
    if myDict[courses[i]][3]:
        new_name=courses[i]+"_lab"
        temp.append(new_name)
courses= []
courses=temp #variables of the problem


slots= []
for i in range(1,64):
    slots.append(i)
domains= {}
for i in range(len(courses)):
    domains[courses[i]]=slots   #domains of the problem
neighbors= {}
for i in range(len(courses)):
    neighbors[courses[i]]= []
for i in range(len(professors)): #ola ta mathimata xwris auta pou exoun ergasthrio afou ekeina den exoun geitones
    for j in range(len(professors)):
        if (myDict[courses[i]][0]==myDict[courses[j]][0] or myDict[courses[i]][1]==myDict[courses[j]][1] or (myDict[courses[i]][2]==True and myDict[courses[j]][2]==True)) and courses[i]!=courses[j]:
            neighbors[courses[i]].append(courses[j])
exam_timetabling_problem= csp.CSP(courses,domains,neighbors,constraints_function)

#1o erwthma
assignment={}
for i in range(len(courses)):
    index=minimum_remaining_value_sorting(courses,domains)
    exam_timetabling_problem.assign(courses[index],1,assignment)
    while True:
        val= random.randint(1, len(domains[courses[index]]))
        exam_timetabling_problem.unassign(courses[index],assignment)
        exam_timetabling_problem.assign(courses[index],val,assignment)
        removals= exam_timetabling_problem.suppose(courses[index],val)
        if (csp.forward_checking(exam_timetabling_problem,courses[index],val,assignment,removals)):
            break
    del domains[courses[index]]
    courses.remove(courses[index])
display_program(assignment)
#print(assignment)
#print(constraints_function('Τεχνητή Νοημοσύνη ΙΙ (ΤΟ ΔΕΥΤΕΡΟ ΚΑΛΥΤΕΡΟ!!!)_lab',assignment['Τεχνητή Νοημοσύνη ΙΙ (ΤΟ ΔΕΥΤΕΡΟ ΚΑΛΥΤΕΡΟ!!!)_lab'],'Τεχνητή Νοημοσύνη ΙΙ (ΤΟ ΔΕΥΤΕΡΟ ΚΑΛΥΤΕΡΟ!!!',assignment['Τεχνητή Νοημοσύνη ΙΙ (ΤΟ ΔΕΥΤΕΡΟ ΚΑΛΥΤΕΡΟ!!!)']))