
import datetime as dt
import maya
import re

"""
Module to detect certain values from the whois data and ssl certificate
Values to detect: From whois: Creation Date and Updated Date
                  From SSL:  Issuer_organizationName(Let's Encrypt the only free certificate so far)
"""  


def whois_characteristics(dicc = {}):
    """
    Return three state depending on the timelapse between the creation date and the current date:
        1_ Not reference for a creation date
        2_ less than a week
        3_ bigger than a week and less or equal than a month
        4_ bigger than a month
    """
    current_date = dt.datetime.now().date()
    
    try:
        response  = dicc['Domain Whois Record']
    except :
        return [0,0]
    else:
        for keyword in response.keys():
            if re.search('Creation Date',keyword):
                delta = current_date - date_parse(response[keyword])
                return set_whois_state(delta.days)
            elif re.search('Created',keyword):
                delta = current_date - date_parse(response[keyword])
                return set_whois_state(delta.days)
            else:
                pass
        return [0,0]
    

def ssl_issuer (dicc = {}):
    """
    Return four states depending on the result of the ssl certificated:
        1_ There is not a ssl certificate 
        2_ There is a ssl certificate and does not correspond to Let's Encryp
        3_ There is a ssl certificate and correspond to Let's Encryp
    """
    if dicc == {} or dicc == {"":""}:
        return [0,0]
    else:
        issuer = dict(x[0] for x in dicc['issuer']) #return a tuple
        issued_by = issuer['organizationName'] 
        if issued_by == "Let's Encrypt":
            return [1,1]
        else:
            return [1,0]


def date_parse(date=""):
    try:
        date_obj = maya.parse(date).datetime()
    except ValueError:
        pass
    else:
        return date_obj.date()
    #-----------------custom function---------
    try:
        date_obj = dt.datetime.strptime(date,"%Y%M%D")
    except ValueError:
        return dt.datetime.now().date()
    else:
        return date_obj.date()


def set_whois_state(delta=0):
    if delta == 0:
        return [0,0]
    elif delta <= 7:
        return [0,1]
    elif delta > 7 and delta <= 30:
        return [1,0]
    else:
        return [1,1]







