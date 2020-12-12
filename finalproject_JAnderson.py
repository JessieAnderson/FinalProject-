"""
File: finalproject_JAnderson.py
Author: Jessie Anderson
A subsidized usuage limit applies (SULA) calculator that determines
if the borrower can receive subsidized loan.
"""

from breezypythongui import EasyFrame
from datetime import datetime
from datetime import date
import tkinter.filedialog



programDict = {"AA":"2","RN":"2","LPN":"1.5","AMT":"3","MT":"1"}


class SulaCalculator(EasyFrame):
    """Subsidized loan calculator based on previous subsidized usage, length
        of program, enrollment, etc."""

    def __init__(self):
        """Sets up the window, widget, and data"""
        EasyFrame.__init__(self, title="SULA Calculator")
        #Create and add widgets to the window
        #Student ID 
        self.addLabel(text = "Student ID:", row=0, column = 0)
        self.studentIDField=self.addTextField(text = "", row = 0, column = 1)

        #Program
        self.addLabel(text = "Program:", row=1, column = 0)
        self.programField=self.addTextField(text = "", row = 1, column = 1)

        #Label Max SULA 
        self.addLabel(text = "Max years of sub: ", row=0, column = 2, sticky ="NSEW")
        self.maxYearsField=self.addFloatField(0.0, row = 1, column = 2,
                                               precision = 2, state="readonly")
        
        #Subsidized loan used 
        self.addLabel(text = "Subsidized Used:", row=2, column = 0)
        self.subsidizedUsedField=self.addFloatField("", row = 2, column = 1,
                                               precision = 2)

        #Compute SULA Years Button
        self.computeYearsButton = self.addButton(text = "Enter", row = 2,
                                         column = 2, command = self.computeSULA)

        #Error message box
        self.sulaErrorField = self.addTextField("", row = 3, column = 0,
                                                state ="readonly", columnspan = 3, sticky ="NSEW")
        
        #Label Beginning and End Dates
        self.addLabel(text = "Beginning and End Dates: Format = (YYYY/MM/DD)", row=4, column = 1, columnspan=2,
                      sticky ="NSEW")
        
        #Fall dates
        self.addLabel(text = "Fall:", row=5, column = 0)
        self.fallBeginField=self.addTextField(text = "2020/08/24", row = 5, column = 1)
        self.fallEndField=self.addTextField(text = "2020/12/19", row = 5, column = 2)
        
        #Spring dates
        self.addLabel(text = "Spring:", row=6, column = 0)
        self.springBeginField=self.addTextField(text = "2021/01/11", row = 6, column = 1)
        self.springEndField=self.addTextField(text = "2021/05/14", row = 6, column = 2)
        
        #Fall Spring Summer label
        self.addLabel(text = "Fall", row=7, column = 1)
        self.addLabel(text = "Spring", row=7, column = 2)
        
        #Enrollment level 
        self.addLabel(text = "Credits:", row=8, column = 0)
        self.fallCreditsField=self.addFloatField("12", row = 8, column = 1,
                                               precision = 2)
        self.springCreditsField=self.addFloatField("12", row = 8, column = 2,
                                               precision = 2)
      
        #Output of 150% calculation of length of program
        self.addLabel(text = "Max Sub Eligibility", row=9, column=0)
        self.maxSubField=self.addFloatField(0, row=9, column = 1,precision = 2,
                                    state="readonly")
        

        #Compute SULA Button
        self.computeSULAButton = self.addButton(text = "Enter", row = 9,
                                         column = 2, command = self.computeSULAUse)
        
        #Fall Spring Summer label 
        self.addLabel(text = "Fall", row=10, column = 1, sticky ="NSEW")
        self.addLabel(text = "Spring", row=10, column = 2, sticky ="NSEW")
        
        #EFC 
        self.addLabel(text = "EFC:", row=11, column = 0)
        self.fallEFCField=self.addFloatField(0, row = 11, column = 1,
                                               precision = 2)
        self.springEFCField=self.addFloatField(0, row = 11, column = 2,
                                               precision = 2)

        #Need Based Aid
        self.addLabel(text = "Need Based Aid:", row=12, column = 0)
        self.fallNeedBasedField=self.addFloatField(0, row = 12, column = 1,
                                               precision = 2)
        self.springNeedBasedField=self.addFloatField(0, row = 12, column = 2,
                                               precision = 2)

        #Non-Need Based Aid
        self.addLabel(text = "Non-Need Based Aid:", row=13, column = 0)
        self.fallNonNeedBasedField=self.addFloatField(0, row = 13, column = 1,
                                               precision = 2)
        self.springNonNeedBasedField=self.addFloatField(0, row = 13, column = 2,
                                               precision = 2)

        #Compute Button
        self.computeButton = self.addButton(text = "Enter", row = 16,
                                         column = 2, command = self.compute)
        
        #Fall Spring label
        self.addLabel(text = "Fall", row=17, column = 1, sticky ="NSEW")
        self.addLabel(text = "Spring", row=17, column = 2, sticky ="NSEW")
                
        #Amount of sub that can be processed
        self.addLabel(text = "Sub Amount To Process:", row=18, column = 0)
        self.fallSubEligField=self.addFloatField("", row = 18, column = 1,
                                               precision = 2)
        self.springSubEligField=self.addFloatField("", row = 18, column = 2,
                                               precision = 2)
        
        #Label for 3rd sub determination
        self.statusField = self.addTextArea(row=19, column = 0,
                                    columnspan = 3, height = 1, width = 12, text = "")

        #Open a text file
        self.openButton = self.addButton(text = "Open", row = 21,
                                         column = 0, command = self.openFile)

        #Save a text file
        self.saveButton = self.addButton(text = "Save",
                                        row = 21, column = 1,
                                        command = self.saveFile)

        #Rest the entries
        self.newButton = self.addButton(text = "New",
                                        row = 21, column = 2,
                                        command = self.newFile)

        #text field and save file name
        self.addLabel(text = "File Name:", row = 0, column = 4)
        self.fileNameField = self.addTextField(text = "", row = 1, column = 4)
        self.textEditField = self.addTextArea(row = 2, column = 4, text = "", rowspan = 5, width = 10)

        
    def computeSULA(self):
        """Computes number of years student can receive in subsidized loan
        based on length of program"""
        sulaRate = 1.5
        programName = self.programField.getText()
        programLength=programDict[programName]
        programL=float(programLength)
        maxSub = sulaRate*programL
        self.maxYearsField.setNumber(maxSub)
        subUsed = self.subsidizedUsedField.getNumber()
        subLeft = maxSub-float(subUsed) #Determines how much sub is left
        #1.5*program length-sub already used
        if (subLeft <=0):
            self.sulaErrorField.setText("Out of subsidized loan due to SULA.")
        
    def computeSULAUse(self):
        #calculate number of days between dates
        try:
            fallBeginText = self.fallBeginField.getText()
            fallBegin=datetime.strptime(fallBeginText,'%Y/%m/%d')
            fallEndText = self.fallEndField.getText()
            fallEnd=datetime.strptime(fallEndText,'%Y/%m/%d')

            springBeginText = self.springBeginField.getText()
            springBegin=datetime.strptime(springBeginText,'%Y/%m/%d')
            springEndText = self.springEndField.getText()
            springEnd=datetime.strptime(springEndText,'%Y/%m/%d')
        except ValueError:
            self.messageBox(title = "ERROR",
                            message = "Date has to be entered YYYY/MM/DD.")

       #determine which semester(s) to use
       #Loan processed in Fall and/or Spring academic year
        fsDaysAcadem = springEnd - fallBegin
        fsDaysAcademic=fsDaysAcadem.days
        fallCredits=self.fallCreditsField.getNumber()
        springCredits=self.springCreditsField.getNumber()
        #Spring only
        if(fallCredits == 0 and springCredits != 0):
            #calculates for full sub
            if (float(springCredits) >= 12):
                springSulaPercent= 1
            elif(float(springCredits) >=9):
                springSulaPercent= 0.8
            elif(float(springCredits) >= 6):
                springSulaPercent= 0.5
            else:
                springSulaPercent= 0

            subAlreadyUsed = self.subsidizedUsedField.getNumber()
            maxSub=self.maxYearsField.getNumber()
            fsd=springSulaPercent+subAlreadyUsed
            if ((springSulaPercent + subAlreadyUsed)>maxSub):
                #if full sub will put student over, calculates for $1 less
                springLoanPeriod = springEnd - springBegin
                spLoanPeriod = springLoanPeriod.days
                usagePeriod = spLoanPeriod/fsDaysAcademic
                if (float(springCredits) >= 12):
                    springLessSulaPercent= 1*usagePeriod
                elif(float(springCredits) >=9):
                    springLessSulaPercent= 0.8*usagePeriod
                elif(float(springCredits) >= 6):
                    springLessSulaPercent= 0.5*usagePeriod
                else:
                    springLessSulaPercent= 0*usagePeriod
                addLessSula = springLessSulaPercent+subAlreadyUsed
                if(addLessSula>maxSub):
                    self.statusField.setText("Not eligible for subsidized loan with current enrollment.")
                else:
                    springSubAmount=4499
                    self.maxSubField.setNumber(springSubAmount)
            else:
                springSubAmount=4500
                self.maxSubField.setNumber(springSubAmount)
                    
        #Fall only
        elif(fallCredits !=0 and springCredits == 0):
            #calculates for full sub
            if (float(fallCredits) >= 12):
                fallSulaPercent= 1
            elif(float(fallCredits) >=9):
                fallSulaPercent= 0.8
            elif(float(fallCredits) >= 6):
                fallSulaPercent= 0.5
            else:
                fallSulaPercent= 0

            subAlreadyUsed = self.subsidizedUsedField.getNumber()
            maxSub=self.maxYearsField.getNumber()
            addSula=fallSulaPercent+subAlreadyUsed
            if ((addSula)>maxSub):
                #if full sub will put student over, calculates for $1 less
                faEnd=fallEnd
                faBegin=fallBegin
                faLoanPeriod = faEnd - faBegin
                fallLoanPeriod=faLoanPeriod.days
                usagePeriod = fallLoanPeriod/fsDaysAcademic
                if (float(fallCredits)>= 12):
                    fallLessSulaPercent= 1*usagePeriod
                elif(float(fallCredits) >=9):
                    fallLessSulaPercent= 0.8*usagePeriod
                elif(float(fallCredits) >= 6):
                    fallLessSulaPercent= 0.5*usagePeriod
                else:
                    fallLessSulaPercent= 0*usagePeriod
                addLessSula = fallLessSulaPercent+subAlreadyUsed
                if(addLessSula>maxSub):
                    self.statusField.setText("Not eligible for subsidized loan with current enrollment.")
                else:
                    fallSubAmount=4499
                    self.maxSubField.setNumber(fallSubAmount)
            else:
                fallSubAmount=4500
                self.maxSubField.setNumber(fallSubAmount)
        #Fall-Spring
        elif(fallCredits != 0 and springCredits != 0):
            #calculates for full sub
            if (float(fallCredits+springCredits) >= 24):
                fallSulaPercent= 1
            elif(float(fallCredits) >=9):
                fallSulaPercent= 0.8
            elif(float(fallCredits) >= 6):
                fallSulaPercent= 0.5
            else:
                fallSulaPercent= 0
                
            if (float(springCredits) >= 12):
                springSulaPercent= 1
            elif(float(springCredits) >=9):
                springSulaPercent= 0.8
            elif(float(springCredits) >= 6):
                springSulaPercent= 0.5
            else:
                springSulaPercent= 0                

            sulaFSused = (fallSulaPercent/2)+(springSulaPercent/2)

            subAlreadyUsed = self.subsidizedUsedField.getNumber()
            maxSub=self.maxYearsField.getNumber()
            if ((sulaFSused + float(subAlreadyUsed))>maxSub):
                #Changes the loan into a Fall only loan
                self.springCreditsField.setNumber = 0
                self.statusField.setText("Cannot get subsdized loan for full year, remove enrollment of the term NOT currently in")
            else:
                fallThruSpringSubAmount=4500
                self.maxSubField.setNumber(fallThruSpringSubAmount)
        
    def compute(self):

        """Determine COA for each semester"""
        fallCredits = self.fallCreditsField.getNumber()
        if (float(fallCredits) >= 12):
            fallCOA=11000
        elif(float(fallCredits) >=9):
            fallCOA=10000
        elif(float(fallCredits) >= 6):
            fallCOA=9000
        elif(float(fallCredits) >1):
            fallCOA = 4000
        else:
            fallCOA = 0

        springCredits = self.springCreditsField.getNumber()
        if (float(springCredits) >= 12):
            springCOA=11000
        elif(float(springCredits) >=9):
            springCOA=10000
        elif(float(springCredits) >= 6):
            springCOA=9000
        elif(float(springCredits) >1):
            springCOA = 4000
        else:
            springCOA = 0
        
        """determine if the student has need"""
        fallEFC = self.fallEFCField.getNumber()
        fallNeed=fallCOA - fallEFC
        if (fallNeed<99):
            self.fallSubEligField.setNumber(0)
            self.statusField.setText("Student doesn't have need.")
        
        #determines if the student has need
        fallNeedAid = self.fallNeedBasedField.getNumber()
        fallNeedAidLeft = fallNeed-fallNeedAid
        maxSubText=self.maxSubField.getNumber()
        maxSub=float(maxSubText)
        if (fallNeedAidLeft<99):
            self.fallSubEligField.setNumber(0)
            self.statusField.setText("There isn't room in the need budget to receive subsidized loan.")
        elif((fallNeedAidLeft-maxSub)<0):
             differenceMaxSub = fallNeedAidLeft-maxSub
             updatedMaxSub = maxSub + differenceMaxSub
             self.maxSubField.setNumber(updatedMaxSub)
                   
        #determines if there is room in COA budget        
        fallNonNeedAid = self.fallNonNeedBasedField.getNumber()
        remainingAid=fallCOA-fallNeedAid-fallNonNeedAid
        if (remainingAid<99):
            self.statusField.setText("There isn't room in the budget to receive subsidized loan.")
        elif((remainingAid -maxSub)<0):
            differenceMaxAid = remainingAid-maxSub
            updatedMaxSub = maxSub+ differenceMaxAid
            self.maxSubField.setNumber(updatedMaxSub)
            self.fallSubEligField.setNumber(updatedMaxSub)
            if(fallCredits != 0 and springCredits != 0):
                 dividedMaxSub = updatedMaxSub/2
                 self.fallSubEligField.setNumber(dividedMaxSub)
        else:
            self.fallSubEligField.setNumber(maxSub)
            if(fallCredits != 0 and springCredits != 0):
                 dividedMaxSub = maxSub/2
                 self.fallSubEligField.setNumber(dividedMaxSub)
            
        springEFC = self.springEFCField.getNumber()
        springNeed=springCOA - springEFC
        if (springNeed<99):
            self.springSubEligField.setNumber(0)
            self.statusField.setText("Student doesn't have need.")

        springNeedAid = self.springNeedBasedField.getNumber()
        springNeedAidLeft = springNeed-springNeedAid
        maxSubText=self.maxSubField.getNumber()
        maxSub=float(maxSubText)
        if (springNeedAidLeft<99):
            self.springSubEligField.setNumber(0)
            self.statusField.setText("There isn't room in the need budget to receive subsidized loan.")
        elif((springNeedAidLeft-maxSub)<0):
             differenceMaxSub = springNeedAidLeft-maxSub
             updatedMaxSub = maxSub + differenceMaxSub
             self.maxSubField.setNumber(updatedMaxSub)
              
        #determines if there is room in COA budget
        fallCredits=self.fallCreditsField.getNumber()
        springCredits=self.springCreditsField.getNumber()  
        springNonNeedAid = self.fallNonNeedBasedField.getNumber()
        #remainingAid=springCOA-springNeedAid-springNonNeedAid
        remainingAidNon=remainingAid-springNonNeedAid
        if (remainingAidNon<99):
            self.statusField.setText("There isn't room in the budget to receive subsidized loan.")
        elif((remainingAidNon -maxSub)<0):
            differenceMaxAid = remainingAidNon-maxSub
            updatedMaxSub = maxSub+ differenceMaxAid
            self.maxSubField.setNumber(updatedMaxSub)
            self.springSubEligField.setNumber(updatedMaxSub)
            if(fallCredits != 0 and springCredits != 0):
                 dividedMaxSub = updatedMaxSub/2
                 self.springSubEligField.setNumber(dividedMaxSub)
        else:
            self.springSubEligField.setNumber(maxSub)
            if(fallCredits != 0 and springCredits != 0):
                 dividedMaxSub = maxSub/2
                 self.springSubEligField.setNumber(dividedMaxSub)
                 
    def openFile(self):
        """Opens text files"""
        fList = [("Python files", "*.py"),("Text files", "*.txt")]
        fileName = tkinter.filedialog.askopenfilename(parent=self,filetypes=fList)
        if fileName !="":
            file=open(fileName, 'r')
            text=file.read()
            file.close()
        self.textEditField.setText(text)
        self.setTitle(fileName)

    def saveFile(self):
        """Saves text files"""
        fList = [("Python files", "*.py"),("Text files", "*.txt")]
        fileName = tkinter.filedialog.asksaveasfilename(parent=self,filetypes=fList,
                                                    initialfile=self.fileNameField.getText(),
                                                    defaultextension = ".txt")
        if fileName !="":
            self.setTitle(fileName)
            file=open(fileName, "w")
            text=self.textEditField.getText()
            file.write(text)
            file.close()

    def newFile(self):
        #Clears text box
        self.studentIDField.setText("")
        self.programField.setText("")
        self.maxYearsField.setNumber(0.0)
        self.subsidizedUsedField.setNumber(0)
        self.sulaErrorField.setText("")
        self.fallCreditsField.setNumber(12)
        self.springCreditsField.setNumber(12)
        self.maxSubField.setNumber(0)
        self.fallEFCField.setNumber(0)
        self.springEFCField.setNumber(0)
        self.fallNeedBasedField.setNumber(0)
        self.springNeedBasedField.setNumber(0)
        self.fallNonNeedBasedField.setNumber(0)
        self.springNonNeedBasedField.setNumber(0)
        self.fallSubEligField.setNumber(0)
        self.springSubEligField.setNumber(0)
        self.statusField.setText("")
        self.textEditField.setText("")
        
                 
def main():
    """Instantiate and pop up the window"""
    SulaCalculator().mainloop()

if __name__ == "__main__":
    main()
