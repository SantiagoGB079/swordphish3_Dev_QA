import xml.dom
from lxml import html
import requests
import cssselect


class Dom():
    def __init__(self,html,links):
        self.html = html
        self.links = links

    #def __str__(self):
    #    return str({"forms":str([self.html.forms[i].action for i in range(0,len(self.html.forms))])})

    def formularios(self):
        """
        Function in charge to return the forms found into the url's html. the function receives an html object
        """
        try:
            self.html.forms
        except:
            return {"forms":0}
        else:
            return {"forms":[self.html.forms[i].action for i in range(0,len(self.html.forms))]}


    @classmethod
    def Url(cls,url):
        try:
            page = requests.get(url,verify=False, timeout=10)
            domhtml = html.fromstring(page.content)
            links = [ i.attrib['href'] for i in domhtml.cssselect('a') if 'href' in i.attrib]
        except:
            domhtml={"forms":0}
            links = []
        return cls(domhtml,links)

    


#obj=Dom.Url('https://moodysmiramar.com/active/online1/login.html')
#print(obj.formularios())