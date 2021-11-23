import re, os, PyPDF2
#Download this file: https://psout.illinoisstate.edu/textbook/isu_textbook_assignments_CURRENT_SP2022.pdf
def main():
    
    if input("If PDF: Input 0, for text file input 1") !=0:
        path = input("Input path to TextbookList.txt:")+r'\textbookList.txt'
        text = openText(path)
    else:
        path = input("Input path to TextbookList.PDF:")+r'\textbookList.txt'
        text = openAndConvertPDF(path)

    results = getTextbooks(text)
    print(results)
    
def openText(path):
    openFile = open(path,'r')
    text = openFile.read()
    openFile.close()
    return text
#Opens The PDF and converts it to a text file-Copy the text and paste it into a txt file for next use
def openAndConvertPDF(path):

    text = ''
    pdfFile = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    for i in range(pdfReader.numPages):
        page = pdfReader.getPage(i)
        text += page.extractText()
    pdfFile.close()
    return text

#Grabs all Class Names, Section Numbers, and ISBN's for textbooks and returns an embedded list    
def getTextbooks(textbookFile):
    results = []
    temp = []
    textbookCheck = False
    firstTime=True
    #The first four pulls the subject, fifth pulls class section, sixth is ISBN, last pulls if there is no textbook assigned
    #At first there was only one for the subject, but some schools use 2 letters(IT), some use 2 numbers, some use both, and the some had 3 spaces inbetween
    everythingAllOfTheTime = re.findall('\w\w\w\s\s\d\d\d|\w\w\s\s\d\d\d|\w\w\s\s\d\d|\w\w\w\s\s\d\d|\w\w\w\s\s\s\d\d|Section:\d\d\d|\d\d\d\d\d\d\d\d\d\d\d\d\d|No Textbook Assigned',textbookFile)

    for i in everythingAllOfTheTime:
        if re.search('\w\w\w\s\s\d\d\d|\w\w\s\s\d\d\d|\w\w\s\s\d\d|\w\w\w\s\s\d\d|\w\w\w\s\s\s\d\d', i) != None:
            if not firstTime:
                print(temp)
                results.append(temp)
                temp = []
            else:
                firstTime = False
        
        temp.append(i)        
    temp.append(i)        
    return results

main()
