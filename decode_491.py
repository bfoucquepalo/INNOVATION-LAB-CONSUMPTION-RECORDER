import json
import xlsxwriter
#
sourceFile = 'gr491/gr491.json'
targetFile = 'gr491/template_gr491.xlsx'
workbook = xlsxwriter.Workbook(targetFile)


with open(sourceFile) as json_file:
    data = json.load(json_file)

    #print(data)
    for currentDomain in data:
        #print(currentDomain)
        myDomain = currentDomain
        worksheet = workbook.add_worksheet(myDomain)
        #We write the header
        myListTitle = ['domain', 'id','title','category','odd','impacts_people','impacts_planet','impacts_prosperity','difficulty','priority','life_cycle','test','description','score (0-100)']
        cell_format = workbook.add_format({'bold': True})
        cell_format.set_bg_color('gray')
        for col_num , dataRow in enumerate(myListTitle):
            worksheet.write(0, col_num, dataRow,cell_format)


        counterLine =0
        for currentQuestion in data[myDomain]:
            counterLine+=1
            #print(currentQuestion['id'])
            myId = currentQuestion['id']
            myTitle = currentQuestion['title']
            myCategory = currentQuestion['category']
            myOdd = ",".join(currentQuestion['odd'])
            myImpactsPeople = currentQuestion['impacts'][0]
            myImpactPlanet = currentQuestion['impacts'][1]
            myImpactPprosperity = currentQuestion['impacts'][2]
            myDifficulty = currentQuestion['difficulty']
            myPriority = currentQuestion['priority']
            myLife_cycle = currentQuestion['life_cycle']
            myTest = currentQuestion['test']
            myDescription = currentQuestion['description']
            myListInfo = [myDomain, myId,myTitle,myCategory,myOdd,myImpactsPeople,myImpactPlanet,myImpactPprosperity,myDifficulty,myPriority,myLife_cycle,myTest,myDescription,'']
            
            #print(myListInfo)
            try:
                for col_num , dataRow in enumerate(myListInfo):
                    worksheet.write(counterLine, col_num, dataRow)
            except Exception as e:
                print(e)

workbook.close()