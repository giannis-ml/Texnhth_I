from datetime import date
import pandas as pd
import random
import csp
import math


def constraints_function(A, a, B, b):
    if(myDict[A][0]==myDict[B][0] and (math.ceil((a+1)/3)!= math.ceil((b+1)/3))):
        return True
    if(myDict[A][1]==myDict[B][1] and (math.ceil((a+1)/3)!= math.ceil((b+1)/3))):
        return True
    if((myDict[A][2]==True and myDict[B][2]==True)and(math.ceil((b+1)/3)-math.ceil((a+1)/3)>=2 or math.ceil((a+1)/3)-math.ceil((b+1)/3)>=2)):
        return True
    if((myDict[A]==True and csp.neighbors[B]==A and b==a+1) or (myDict[B]==True and csp.neighbors[A]==B and a==b+1)):
        return True
    return False

class Timetabling(csp.CSP):

    def __init__(self,courses,semesters,professors,difficultly,labs,myDict,slots):
        self.variables = courses
        self.domains= {}
        for i in range(len(courses)):
            self.domains[courses[i]]=slots
        self.neighbors= {}
        for i in range(len(courses)):
            self.neighbors[courses[i]]= []
        labs_counter=0
        for i in range(len(professors)):
            for j in range(len(professors)):
                if (myDict[courses[i]][0]==myDict[courses[j]][0] or myDict[courses[i]][1]==myDict[courses[j]][1] or (myDict[courses[i]][2]==True and myDict[courses[j]][2]==True)) and courses[i]!=courses[j]:
                    self.neighbors[courses[i]].append(courses[j])
            if(myDict[courses[i]][3]==True):
                self.neighbors[courses[len(professors)+labs_counter]].append(courses[i])
                labs_counter+=1
    
                
        csp.CSP.__init__(self,self.variables,self.domains,self.neighbors,constraints_function)

    def display(self):
        output = csp.min_conflicts(self)
        for i in output:
            if(output[i]%3==0):
                time="9-12"
            elif(output[i]%3==1):
                time="12-3"
            else:
                time="3-6"
            print (i," Mέρα εξέτασης:",math.ceil((output[i]+1)/3),"Ώρα εξέτασης: ",time)

if __name__ == "__main__":
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
            myDict[new_name]=[]
            myDict[new_name].append(myDict[courses[i]])
            myDict[new_name].append(myDict[courses[i]])
            myDict[new_name].append(myDict[courses[i]])
            myDict[new_name].append(myDict[courses[i]])
    courses= []
    courses=temp
    temp=[]
    for i in semesters:
        temp.append(i)
    semesters= []
    semesters=temp
    temp= []
    for i in professors:
        temp.append(i)
    professors= []
    professors=temp
    temp= []
    for i in difficultly:
        temp.append(i)
    difficultly= []
    difficultly=temp
    temp= []
    for i in labs:
        temp.append(i)
    labs= []
    labs=temp
    slots= []
    for i in range(1,64):
        slots.append(i)
    examination_of_di = Timetabling(courses,semesters,professors,difficultly,labs,myDict,slots)
    csp.backtracking_search(examination_of_di, csp.mrv, csp.lcv , csp.forward_checking)
    #examination_of_di.display()