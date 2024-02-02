from lxml import etree
import json
import sys
from datetime import datetime

class BuildingBlock:
    def __init__(self):
        pass
    def __init__(self,identifier,name,abstract,status,dateTimeAddition,itemClass,register,version,maturity):
        self.identifier = identifier
        self.name = name
        self.abstract = abstract
        self.status = status
        self.dateTimeAddition = dateTimeAddition
        self.itemClass = itemClass
        self.register = register
        self.version = version
        self.maturity = maturity


def main(argv):

    # python3 processor.py 22-047r1.html https://docs.ogc.org/is/22-047r1/22-047r1.html http://www.opengis.net/spec/geosparql/1.1 
    # python3 processor.py 22-003.html https://docs.ogc.org/is/22-003/22-003.html http://www.opengis.net/spec/ogcapi-movingfeatures-1/1.0

    baseURI = argv[2]
    source_webpage = argv[1]
    document_number = str(argv[0]).lower().replace(".html","")  

    wd = "./"



    fout = open(wd+document_number+'.csv','w')

    bb_list = []

    with open(wd+document_number+".html",'r') as file:
        data = file.read()
        table = etree.HTML(str(data)).findall(".//table")
        rows = iter(table)
        headers = [col.text for col in next(rows)]
        for row in rows:
            outputstring = ''
            date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            bb = BuildingBlock('identifier','name', 'abstract', 'under-development', str(date_time), 'api', 'ogc-building-block-register', '1.0.0','development')
            modSpecElementType = None
            if 'class' in row.attrib:
                if row.attrib['class'] == 'modspec':
                    paragraphs = row.findall(".//p")
                    for paragraph in paragraphs:
                        if 'class' in paragraph.attrib:
                            if paragraph.attrib['class'] == 'RecommendationTitle':
                                if 'id' in row.attrib:
                                    outputstring = outputstring +""+ source_webpage+"#"+str(row.attrib['id'])
                                bb.name = str(paragraph.text)
                                modSpecElementType = 'modSpecElement'
                                #print(paragraph.text)
            if str(modSpecElementType) == 'modSpecElement':
                trElements = row.findall(".//tr")
                for trElement in trElements:
                    thElements = trElement.findall(".//th")
                    for thElement in thElements:
                        if str(thElement.text) == 'Identifier':
                            tdElements = trElement.findall(".//td")
                            for tdElement in tdElements:
                                ttElements = tdElement.findall(".//tt")
                                for ttElement in ttElements:
                                    if "www.opengis.net" in str(ttElement.text):
                                        outputstring = outputstring +","+str(ttElement.text)+""
                                    else:
                                        outputstring = outputstring +","+baseURI+ str(ttElement.text)+""
                                    bb.identifier = str(ttElement.text)
            if(len(outputstring)>0):
                fout.write(outputstring+"\n")
                print(outputstring+"\n")
                bb_list.append(bb)

    fout.close()


if __name__ == "__main__":
   main(sys.argv[1:])
