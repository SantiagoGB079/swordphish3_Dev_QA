"""
Module to parse the whois reponse into a dictionay, removing the unuseful information
"""

import json
import io
import re 

#Text to capture query's response and store it in a json format
#whois archive "whois.text"

def dictionary(data = ''):
    """
    Method to convert the data entered into a dictionary
    Arguments:
    data: Information to be stored into a dictionary
    """

    if data == '':
        return {}
    else:
        lineas = data 
    dicc = {}

    #we first analize the lines in order to remove unuseful data
    for line in lineas:
    
        if line.split(':',maxsplit=1)[0].count(' ') < 6 and line.count(':') < 1  or line.count(':') != 0 :
            
            lista = line.replace('\n','',1).split(':',maxsplit=1)

            if len(lista) > 1 :
                try:
                    dicc[str(lista[0])] 
                except (NameError,KeyError):
                    dicc[str(lista[0])] = str(lista[-1]).strip()
                else:
                    if str(lista[-1]) == '' or str(lista[-1]) == None:
                        pass
                    else:
                        aux = str(lista[-1]).strip() + ' , ' + str(dicc.get(lista[0]))
                        dicc[lista[0]] = aux
            else:
                try:
                    dicc['Other'] 
                except (NameError,KeyError):
                    dicc['Other'] = str(lista[0]).strip()
                else:
                    if str(lista[-1]) == '' or str(lista[-1]) == None:
                        pass
                    else:
                        aux = str(lista[-1]).strip() + ' , ' + str(dicc.get('Other'))
                        dicc['Other'] = aux

    return dicc


def jsonparser(data = '' , dict = {}, keyword = ''):
    """
    Method to return a dictionary with the data entered. This method is made to parse the data returned from the whois command.
    This method has tree arguments:
    data(Mandatory): information to be store into a dictionary
    dict(Optional): Use if you want to add new information to an existed dictionary
    keyword(Optional): This argument is used if you want to group the information entered into a single keyword.
    """
    
    if data != '':
        
        lineas = data.split('\n')

        if dict == {}:
            dicc = {}
        else:
            dicc = dict
    
        if keyword == '':
            dicc = dictionary(lineas)
        else:
            dicc[keyword] = dictionary(lineas)
            
        try:
            del dicc["Other"]
        except:
            pass
        return dicc
    else:
        return {}    

    
          
#print(aux) 
#Funcion recursiva
#def jsonparser(filename = 'name', dict = {}, keyword = ''):
#a = jsonparser(filename = 'whois.txt',dict = jsonparser(filename='whoisip.txt',keyword='Network Whois Record'),keyword='Domain Whois Record')
#print(a)
#json = json.dumps(a)
#print(json)  



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    






