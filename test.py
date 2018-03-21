from zeep import Client
import xml.etree.ElementTree as ET

client = Client("http://fws.cs.ui.ac.id/RESTFulWSStanfordPOSTagger/POSTagger?wsdl")

response = client.service.getPOSTag("saya makan nasi")
tree = ET.fromstring(response)
print(ET.tostring(tree, encoding='utf8', method='xml'))
