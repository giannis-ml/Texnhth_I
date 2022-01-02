import pandas as pd 
import csp

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
courses=temp


slots= []
for i in range(1,64):
    slots.append(i)
domains= {}
for i in range(len(courses)):
    domains[courses[i]]=slots
neighbors= {}
for i in range(len(courses)):
    neighbors[courses[i]]= []
for i in range(len(professors)): #ola ta mathimata xwris auta pou exoun ergasthrio afou ekeina den exoun geitones
    for j in range(len(professors)):
        if (myDict[courses[i]][0]==myDict[courses[j]][0] or myDict[courses[i]][1]==myDict[courses[j]][1] or (myDict[courses[i]][2]==True and myDict[courses[j]][2]==True)) and courses[i]!=courses[j]:
            neighbors[courses[i]].append(courses[j])


# def constraints_function(A, a, B, b):
#     if 