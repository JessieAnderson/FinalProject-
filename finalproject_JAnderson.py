"""
File: finalproject_JAnderson.py
Author: Jessie Anderson
A subsidized usuage limit applies (SULA) calculator that determines
if the borrower can receive subsidized loan.
"""

from breezypythongui import EasyFrame
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
        #Student ID 0
        self.addLabel(text = "Student ID:", row=0, column = 0)
        self.studentIDField=self.addFloatField(0.0, row = 0, column = 0,
                                               width = 15,precision = 2)
        #Program 1
        self.addLabel(text = "Program:", row=1, column = 0)
        self.programField=self.addTextField(text = "", row = 1, column = 0,
                                               width = 15)

        #Label Max SULA 1
        self.addLabel(text = "Max years of sub: ", row=1, column = 1, sticky ="NSEW")
        self.maxYearsField=self.addFloatField(0.0, row = 2, column = 1,
                                               width = 15,precision = 2)
        
        #Subsidized loan used 2
        self.addLabel(text = "Subsidized Used:", row=2, column = 0)
        self.subsidizedUsedField=self.addFloatField(0.0, row = 2, column = 0,
                                               width = 15,precision = 2)

        #Compute SULA Years Button
        self.computeYearsButton = self.addButton(text = "Enter", row = 3,
                                         column = 1, command = self.computeSULA)
        
        #label for 1st sub determination 3
        self.addLabel(text = "", row=4, column = 0, columnspan = 2, sticky ="NSEW")
        
        #Label Beginning and End Dates 4
        self.addLabel(text = "Beginning and End Dates: Format = (YYYY,MM,DD)", row=5, column = 0, columnspan=2,
                      sticky ="NSEW")
        #Fall dates 5
        self.addLabel(text = "Fall:", row=6, column = 0)
        self.fallBeginField=self.addTextField(text = "", row = 6, column = 0,
                                               width = 15)
        self.fallEndField=self.addTextField(text = "", row = 6, column = 1,
                                               width = 15)
        
        #Spring dates 6
        self.addLabel(text = "Spring:", row=7, column = 0)
        self.springBeginField=self.addTextField(text = "", row = 7, column = 0,
                                               width = 15)
        self.springEndField=self.addTextField(text = "", row = 7, column = 1,
                                               width = 15)
        
        #Summer dates 7
        self.addLabel(text = "Summer:", row=8, column = 0)
        self.summerBeginField=self.addTextField(text = "", row = 8, column = 0,
                                               width = 15)
        self.summerEndField=self.addTextField(text = "", row = 8, column = 1,
                                               width = 15)
        
        #Fall Spring Summer label 8
        self.addLabel(text = "Fall", row=9, column = 0, sticky ="NSEW")
        self.addLabel(text = "Spring", row=9, column = 1, sticky ="NSEW")
        self.addLabel(text = "Summer", row=9, column = 2, sticky ="NSEW")
        
        #Enrollment level 9
        self.addLabel(text = "Credits:", row=10, column = 0)
        self.fallCreditsField=self.addFloatField(0.0, row = 10, column = 0,
                                               width = 9,precision = 2)
        self.springCreditsField=self.addFloatField(0.0, row = 10, column = 1,
                                               width = 9,precision = 2)
        self.summerCreditsField=self.addFloatField(0.0, row = 10
                                                   , column = 2,
                                               width = 9,precision = 2)
        
        #label for 2nd sub determination 10
        self.addLabel(text = "", row=11, column = 0, columnspan = 2, sticky ="NSEW")

        #Compute SULA Button
        self.computeSULAButton = self.addButton(text = "Enter", row = 12,
                                         column = 1, command = self.computeSULAUse)
        
        #Fall Spring Summer label 11
        self.addLabel(text = "Fall", row=13, column = 0, sticky ="NSEW")
        self.addLabel(text = "Spring", row=13, column = 1, sticky ="NSEW")
        self.addLabel(text = "Summer", row=13, column = 2, sticky ="NSEW")
        
        #EFC 12
        self.addLabel(text = "EFC:", row=14, column = 0)
        self.fallEFCField=self.addFloatField(0.0, row = 14, column = 0,
                                               width = 9,precision = 2)
        self.springEFCField=self.addFloatField(0.0, row = 14, column = 1,
                                               width = 9,precision = 2)
        self.summerEFCField=self.addFloatField(0.0, row = 14
                                                   , column = 2,
                                               width = 9,precision = 2)
        
        #Need Based Aid 13
        self.addLabel(text = "Need Based Aid:", row=15, column = 0)
        self.fallNeedBasedField=self.addFloatField(0.0, row = 15, column = 0,
                                               width = 9,precision = 2)
        self.springNeedBasedField=self.addFloatField(0.0, row = 15, column = 1,
                                               width = 9,precision = 2)
        self.summerNeedBasedField=self.addFloatField(0.0, row = 15
                                                   , column = 2,
                                               width = 9,precision = 2)
        
        #Non-Need Based Aid 14
        self.addLabel(text = "Non-Need Based Aid:", row=16, column = 0)
        self.fallNonNeedBasedField=self.addFloatField(0.0, row = 16, column = 0,
                                               width = 9,precision = 2)
        self.springNonNeedBasedField=self.addFloatField(0.0, row = 16, column = 1,
                                               width = 9,precision = 2)
        self.summerNonNeedBasedField=self.addFloatField(0.0, row = 16,
                                                column = 2, width = 9,precision = 2)
        
        #label for sub and unsub 15
        self.addLabel(text = "Subsidized", row=17, column = 0, sticky ="NSEW")
        self.addLabel(text = "Unsubsidized", row=17, column = 1, sticky ="NSEW")
        
        #Yearly loan amount 16
        self.addLabel(text = "Yearly Loan Amount:", row=18, column = 0)
        self.subYearlyField=self.addFloatField(0.0, row = 18, column = 0,
                                               width = 15,precision = 2)
        self.unsubYearlyField=self.addFloatField(0.0, row = 18, column = 1,
                                               width = 15,precision = 2)
        
        #Lifetime loan amount 17
        self.addLabel(text = "Lifetime Loan Amount:", row=19, column = 0)
        self.subLifetimeField=self.addFloatField(0.0, row = 19, column = 0,
                                               width = 15,precision = 2)
        self.unsubLifetimeField=self.addFloatField(0.0, row = 19, column = 1,
                                               width = 15,precision = 2)
        

        #label for 3rd sub determination 18
        self.statusField = self.addTextField(row=20, column = 0,
                                    columnspan =2, text = "", state="readonly", sticky ="NSEW")

        #Compute Button
        self.computeButton = self.addButton(text = "Enter", row = 21,
                                         column = 1, command = self.compute)
    def computeSULA(self):
        """Computes number of years student can receive in subsidized loan
        based on length of program"""
        """sulaRate = 1.5
        programName = self.programField.getText
        print(programName)"""
        #programLength=[programDict[pLength(y)] for y in programName]
        #for (programName,value) in programDict():
        #print(programDict[self.programField.setText])
            #print(programName, value)
        #self.maxYearsField.setText(programLength)
        """for pName, pLength in programDict.items():
            if pName == programName:
                print(pLength)"""
        
    def computeSULAUse(self):
        #calculate number of days between dates
        fallBegin = int(self.fallBeginField.getText)
        fallEnd = self.fallEndField.getText

        springBegin = self.springBeginField.getText
        springEnd = int(self.springEndField.getText)

        summerBegin = self.summerBeginField.getText
        summerEnd = self.summerEndField.getText

       #determine which semester(s) to use
       #Loan processed in Fall and/or Spring academic year
        fsDaysAcademic = springEnd.days - fallBegin.days
       #Summer loan
        if (summerBegin != ""):
           sLoanPeriod = summerEnd()- summerBegin()
           sDaysAcademic = summerEnd() - fallBegin()
        #Spring only
        elif(fallEnd() == "" and springBegin() != ""):
            spLoanPeriod = springEnd() - springBegin()
            spOnlySULA = spLoanPeriod/fsDaysAcademic
        #Fall only
        elif(fallEnd() !="" and springBegin() == ""):
            faLoanPeriod = fallEnd() - fallBegin()
            faOnlySULA = faLoanPeriod/fsDaysAcademic
        elif(fallEnd() !="" and springBegin() !=""):
            fsLoanPeriod = springEnd()-fallBegin()
            fsSULA = fsLoanPeriod.days/fsDaysAcademic.days
            

        #calculate usage period
        #days in loan period/days in academic year
        
        
    def compute(self):

        """Determine COA for each semester"""
        fallCredits = self.fallCreditsField.getNumber
        if (fallCredits() >= 12):
            fallCOA=11000
        elif(fallCredits() >=9):
            fallCOA=10000
        elif(fallCredits() >= 6):
            fallCOA=9000
        elif(fallCredits() >1):
            fallCOA = 4000
        else:
            fallCOA = 0

        springCredits = self.springCreditsField.getNumber
        if (springCredits() >= 12):
            springCOA=11000
        elif(springCredits() >=9):
            springCOA=10000
        elif(springCredits() >= 6):
            springCOA=9000
        elif(springCredits() >1):
            springCOA = 4000
        else:
            springCOA = 0

        summerCredits = self.summerCreditsField.getNumber
        if (summerCredits() >= 12):
            summerCOA=11000
        elif(summerCredits() >=9):
            summerCOA=10000
        elif(summerCredits() >= 6):
            summerCOA=9000
        elif(summerCredits() >1):
            summerCOA = 4000
        else:
            summerCOA = 0

        
            """determine if the student has need"""
            fallEFC = self.fallEFCField.getNumber
            fallNeed=fallCOA - fallEFC()
            if (fallNeed<99):
                self.statusField.setText("There isn't enough need to received subsidized loan.")
            

        
            #determines if the student has need
            """fallNeedAid = self.fallNeedBasedField.getNumber()
            fallNeed = fallCOA - fallNeedAid

            springNeedAid = self.springNeedBasedField.getNumber()
            springNeed = springCOA - springNeedAid

            summerNeedAid = self.summerNeedBasedField.getNumber()
            summerNeed = summerCOA - summerNeedAid"""
            fallNeedAid = self.fallNeedBasedField.getNumber()
            fallNeedAidLeft = fallNeed-fallNeedAid
            if (fallNeedAidLeft<99):
                self.statusField.setText("There isn't room in the need budget to receive subsidized loan.")

        
            #determines if there is room in COA budget
            
            fallNonNeedAid = self.fallNonNeedBasedField.getNumber()
            remainingAid=fallCOA-fallNeedAid-fallNonNeedAid

            if (remainingAid<99):
                self.statusField.setText("There isn't room in the budget to receive subsidized loan.")
                
            """fallNonNeed = fallCOA - fallNonNeedAid

            springNonNeedAid = self.springNonNeedBasedField.getNumber()
            springNonNeed = springCOA - springNonNeedAid

            summerNonNeedAid = self.summerNonNeedBasedField.getNumber()
            summerNonNeed = summerCOA - summerNonNeedAid"""            
                 

def main():
    """Instantiate and pop up the window"""
    SulaCalculator().mainloop()

if __name__ == "__main__":
    main()
