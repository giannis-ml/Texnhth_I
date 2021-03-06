from datetime import date
import pandas as pd
import random
import csp
import math

# A function that returns true if neighbors
# A, B satisfy the constraint when they have values A=a, B=b
def constraints_function(csp,A, a, B, b):
    index_of_A= csp.variables.index(A)
    index_of_B= csp.variables.index(B)
    if(a==b):
        return False
    # condition for labs that is not working properly and make program not terminate
    # if (A==(B+"_lab")):
    #     if math.ceil((a+1)/3)!= math.ceil((b+1)/3):
    #         return False
    #     else:
    #         if b-a!=1:
    #             return False
    # if (B==(A+"_lab")):
    #     if math.ceil((b+1)/3)!= math.ceil((a+1)/3):
    #         return False
    #     else:
    #         if a-b!=1:
    #             return False
    # condition for semester constraint
    if(semesters[index_of_A]==semesters[index_of_B]):
        # checks if course A examined in the same day with course B
        if(math.ceil((a+1)/3)== math.ceil((b+1)/3)):
            return False
    # condition for professors constraint
    if((professors[index_of_A]==professors[index_of_B])):
        if(math.ceil((a+1)/3)== math.ceil((b+1)/3)):
            return False
    # condition for difficult courses
    if(difficultly[index_of_A]==True and difficultly[index_of_B]==True):
        if((math.ceil((b+1)/3)-math.ceil((a+1)/3)>=2 or math.ceil((a+1)/3)-math.ceil((b+1)/3)>=2)==False):
            return False
    return True

# function that takes a empty dictionary and returns dictionary with {var:degree}
def compute_degree(csp,deg):
    for i in range(0,len(csp.variables),1):
        counter=0
        for j in range(0,len(csp.variables),1):
            if (csp.variables[i]==(csp.variables[j]+"_lab")):
                counter+=1
            if(semesters[i]==semesters[j]):
                counter+=1
            if((professors[i]==professors[j])):
               counter+=1
            if(difficultly[i]==True and difficultly[j]==True):
                counter+=1
        deg[csp.variables[i]]=counter

# function that takes a empty dictionary and returns dictionary with {var:domain size}
def compute_domain_size(csp,dom):
    for i in csp.variables:
        domain_size=len(csp.domains[i])
        dom[i]=domain_size

# dom/wdeg heuristic that returns variale which minimize the quotient (domain size of the variable)/(degree of the variable)
def dom_wdeg(assignment, csp):
    dom={}
    deg={}
    quotient={}
    compute_degree(csp,deg)
    compute_domain_size(csp,dom)
    for i in csp.variables:
        if i not in assignment:
            quotient[i]= dom[i]/deg[i]
    min_value=min(quotient.values())
    for i in csp.variables:
        if i not in assignment:
            if quotient[i]==min_value:
                return i


        

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
                if i!=j:
                    self.neighbors[courses[i]].append(courses[j])
    
                
        csp.CSP.__init__(self,self.variables,self.domains,self.neighbors,constraints_function)

    def display(self,output):
        for i in output:
            if(output[i]%3==0):
                time="9-12"
            elif(output[i]%3==1):
                time="12-3"
            else:
                time="3-6"
            print (i," M?????? ????????????????:",math.ceil((output[i]+1)/3),"?????? ????????????????: ",time)

if __name__ == "__main__":
    df= pd.read_csv('???????????????? ??????????????????.csv')
    semesters= df['??????????????']
    courses= df['????????????']
    professors= df['??????????????????']
    difficultly= df['?????????????? (TRUE/FALSE)']
    labs= df['???????????????????? (TRUE/FALSE)']
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
    print("\nFORWARD CHECKING\n")
    examination_of_di.display(output)

    output=csp.backtracking_search(examination_of_di, dom_wdeg, csp.lcv , csp.mac )
    print("\nMAC\n")
    examination_of_di.display(output)

    output= csp.min_conflicts(examination_of_di)
    print("\nMIN CONFLICTS\n")
    examination_of_di.display(output)
    