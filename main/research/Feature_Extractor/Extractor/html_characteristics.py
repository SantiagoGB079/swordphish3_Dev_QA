"""
Module to extract some characteristics related to the data provided from  an url's html

Inputs: domain, whois_w and html response
process
Identify urls-
              extract its domains -- compare this domain with the domain in the input
              ignore url related to social networks
              extract whois of the most common domain found and compare with the initial whois
output:     00-same domain and same whois
            01-same domain and different whois (very low probability)
            10-different domain and same whois
            11-different domain and different whois

"""

from main.research.Feature_Extractor import Parser,Extractor
import pandas as pd


def extract_domains(url):
    """
    Function to extract the links into an html
    """
    html = Parser.dom.Dom.Url(url)
    if html.links == []:
        links = []
        set_links = set()
        most_rep_link = ""
    else:
        #urls = [ i.attrib['href'] for i in html.cssselect('a') if 'href' in i.attrib]
        links = [Parser.url_parser.URL(i).domain for i in html.links if i != "" and ("http://" in i or "https://" in i)]
        set_links = set(links)
        most_rep_link = pd.DataFrame(links)[0].value_counts().idxmax()

    return links,set_links,most_rep_link


def whois_important_values(wh={}):
    """
    Obtein some values relevant into the whois
    -Registrant Organization
    -owner
    -Organisation
    """
    for i in wh.values():
        try:
            return i["Registrant Organization"]
        except:
            pass

        try:
            return i["Organisation"]
        except:
            pass

        try:
            return i["owner"]
        except:
            pass

        try:
            return i["Registrant Name"]
        except:
            pass

    return ""


def compare_dom_whois(url="",wh={}):
    """
    function to compare the suspicions domain with the most frecuently domain into its html and their whois values to identify if they have the same registrant
    """

    domain = Parser.url_parser.URL(url).domain
    html_domain = extract_domains(url)[-1]

    wh_dom_found = Extractor.whois_query.Whois()
    whois_dom_found = wh_dom_found.whois(html_domain)

    wh_res = Extractor.parse_response.jsonparser(data=whois_dom_found['w'],dict={},keyword='Domain Whois Record')
    wh_res.update({'Registrar Whois Record' : Extractor.parse_response.jsonparser(data=whois_dom_found['w_server'],dict={},keyword='')})

    dom_wh_organization = whois_important_values(wh)
    dom_wh_found_organization = whois_important_values(wh_res)

    if domain == html_domain:
        if dom_wh_organization == dom_wh_found_organization:
            return [0,0]
        else:
            return [0,1]
    else:
        if dom_wh_organization == dom_wh_found_organization:
            return [1,0]
        else:
            return [1,1]







#test = extract_domains("https://moodysmiramar.com/active/online1/login.html")
#print(test)
