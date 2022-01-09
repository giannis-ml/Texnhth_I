from datetime import date
import pandas as pd
import random
import csp
import math


def constraints_function(csp,A, a, B, b):
    index_of_A= courses.index(A)
    index_of_B= courses.index(B)
    if(A!=B):
        if(a==b):
            return False
    if(semesters[index_of_A]==semesters[index_of_B]):
        if(math.ceil((a+1)/3)== math.ceil((b+1)/3)):
            if (not((labs[index_of_A]==True and csp.neighbors[B][0]==A)or(labs[index_of_B]==True and csp.neighbors[A][0]==B))):
                return False
    if((professors[index_of_A]==professors[index_of_B])):
        if(math.ceil((a+1)/3)== math.ceil((b+1)/3)):
            if (not((labs[index_of_A]==True and csp.neighbors[B][0]==A)or(labs[index_of_B]==True and csp.neighbors[A][0]==B))):
                return False
    if(difficultly[index_of_A]==True and difficultly[index_of_B]==True):
        if((math.ceil((b+1)/3)-math.ceil((a+1)/3)>=2 or math.ceil((a+1)/3)-math.ceil((b+1)/3)>=2)==False):
            return False
    # if(labs[index_of_A]==True):
    #     if(csp.neighbors[B][0]==A):
    #         if(b!=a+1):
    #             return False
    # if(labs[index_of_B]==True):
    #     if(csp.neighbors[A][0]==B):
    #         if(a!=b+1):
    #             return False
    return True

class Timetabling(csp.CSP):

    def __init__(self,courses,semesters,professors,difficultly,labs,slots):
        self.variables = courses
        self.domains= {}
        for i in range(len(courses)):
            self.domains[courses[i]]=slots
        self.neighbors= {}
        for i in range(len(courses)):
            self.neighbors[courses[i]]= []
        labs_counter=0
        courses_with_labs=0
        for i in labs:
            if i==True:
                courses_with_labs+=1
        for i in range(len(courses)):
            for j in range(len(courses)):
                if ((semesters[i]==semesters[j]) or (professors[i]==professors[j]) or (difficultly[i]==True and difficultly[j]==True)) and courses[i]!=courses[j]:
                    self.neighbors[courses[i]].append(courses[j])
            if(labs[i]==True):
                if(labs_counter==courses_with_labs):
                    break
                self.neighbors[courses[len(courses)-courses_with_labs+labs_counter]].append(courses[i])
                labs_counter+=1
    
                
        csp.CSP.__init__(self,self.variables,self.domains,self.neighbors,constraints_function)

    def display(self,output):
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
    temp=[]
    for i in range(len(courses)):
        temp.append(courses[i])
    for i in range(len(courses)):
        if labs[i]==True:
            new_name=courses[i]+"_lab"
            temp.append(new_name)
            semesters.append(semesters[i])
            professors.append(professors[i])
            difficultly.append(difficultly[i])
            labs.append('False')
    courses= []
    courses=temp
    slots= []
    for i in range(1,64):
        slots.append(i)
    examination_of_di = Timetabling(courses,semesters,professors,difficultly,labs,slots)
    output=csp.backtracking_search(examination_of_di, csp.mrv, csp.lcv , csp.forward_checking)
    examination_of_di.display(output)