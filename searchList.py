import yoinkingTextbooks as yoink

def searchTextbookList(className,section):
    path = input(r"Input path to TextbookList.txt:")+r'\textbookList.txt'
    text = yoink.openText(path)
    beegList = yoink.getTextbooks(text)

    smallerList = []
    for i in beegList:
        if className == beegList[beegList.index(i)][0]:
            smallerList.append(i)

    for i in smallerList:
        if section == smallerList[smallerList.index(i)][1]:
            return i

#Debug lines
#className = input('Input Class (With 2 spaces inbetween):')
#section = 'Section:'+str(input('Input Section Number:'))  
#searchTextbookList(className,section)
