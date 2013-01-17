
import sqlite3
import xml.etree.ElementTree as ET


def saveCSV(result):
    with open('../data/dict.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["kanji","kana","entry"])
        writer.writerows(result)

def saveXML(result):
    columnNames = ['kanji', 'kana', 'entry']
    a = ET.Element('a')
    b = ET.SubElement(a, 'b')
    c = ET.SubElement(a, 'c')
    d = ET.SubElement(c, 'd')

conn = sqlite3.connect('../data/dict.sqlite')
c = conn.cursor()
c.execute("select kanji, kana, entry from dict")
result = c.fetchall()
saveCSV(result)