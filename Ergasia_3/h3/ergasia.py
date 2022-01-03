from datetime import date
import pandas as pd
import random
import csp

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
# dates={}
# for i in range(0,len(slots),3):
#     print(21/(i+1))
#     dates[i] = (i%21)+1,"9-12"
#     dates[i+1] = (i%21)+1,"12-3"
#     dates[i+2] = (i%21)+1,"3-6"
#ftiakse esy mia display  function
#print(dates)
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
    val= random.randint(1, len(domains[courses[index]]))
    exam_timetabling_problem.assign(courses[index],val,assignment)
    removals= exam_timetabling_problem.suppose(courses[index],val)
    csp.forward_checking(exam_timetabling_problem,courses[index],val,assignment,removals)
    del domains[courses[index]]
    courses.remove(courses[index])
exam_timetabling_problem.display(assignment)