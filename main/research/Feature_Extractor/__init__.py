"""
Module to find the whois record
"""

from main.research.Feature_Extractor.Extractor import parse_response
from main.research.Feature_Extractor.Extractor import whois_query
from main.research.Feature_Extractor.Extractor import ssl_cert
from main.research.Feature_Extractor.Extractor import extract_characteristics
from main.research.Feature_Extractor.Extractor import html_characteristics
from main.research.Feature_Extractor.Parser import url_parser
from main.research.Feature_Extractor.Parser import dom
from collections import Counter
import re


# Procedure to extract all the whois information through the whois and dig linux command
#
# Find the domain name
# Find the registrar whois server
# Find IP address
# Find whois related to IP address
# Retrive a Json with information gathered

class main():

    def __init__(self, url, label):
        self.url = url
        self.label = label
        self.whois = self.whois()


    def whois(self):
        """
        Method to return the whois information relate to the an url.
        Procedure:
        1.Find the domain name
        2. Find the registrar whois server
        3. Find IP address
        4. Find whois related to IP address
        5. Retrive a Json with information gathered
        """
        print("Starting extraction of "+self.url)
        domain = dom.Dom.Url(self.url)
        urlw = url_parser.URL(self.url)
        wh = whois_query.Whois()

        # /////////////////////////////////
        data = wh.whois(dom=urlw.domain)

        certificate = ssl_cert.ssl_certificate(urlw.domain)
        # /////////////////////////////////
        url = lambda x: len(x)
        pathsfun = lambda x: True if x != 'NaN' else False
        pathsfil = pathsfun(urlw.path)
        paths = lambda x: len(list(filter(pathsfun, x)))
        pathschar = lambda x: 1 if ('$' or '_' or '-' or '&' or '~' or '+' or '=') in str(x) else 2
        domains = lambda x: len(x)

        subdomains = lambda x:len(x)
        """Dominios gTLD no restringidos"""
        tld = ['com', 'info', 'net', 'org']
        """Dominios gTLD restringidos"""
        tld2 = ['biz', 'name', 'pro']
        """Dominios gTLD patrocinados"""
        tld3 = ['aero', 'asia', 'cat', 'coop', 'edu', 'gov', 'int', 'jobs', 'mil', 'mobi', 'museum', 'post', 'tel',
                'travel', 'xxx']
        """Dominios gTLD paises"""
        tld4 = ['ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'aw', 'ax', 'az',
                'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bw', 'by',
                'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 'cv', 'cw',
                'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'er', 'es', 'et', 'eu', 'fi',
                'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq',
                'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in',
                'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr',
                'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md',
                'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx',
                'my', 'mz', 'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe',
                'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru',
                'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'su',
                'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tr', 'tt',
                'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf',
                'ws', 'ye', 'yt', 'za', 'zm', 'zw']

        tlds = lambda x: 1 if x.rsplit('.')[-1] in str(tld) else 0

        tlds2 = lambda x: 1 if x.rsplit('.')[-1] in str(tld2) else 0
        tlds3 = lambda x: 1 if x.rsplit('.')[-1] in str(tld3) else 0
        tlds4 = lambda x: 1 if x.rsplit('.')[-1] in str(tld4) else 0
        verifyip = lambda x: 1 if ((len(re.findall(r"2[0-5][0-5]|1[0-9][0-9]|[0-9][0-9]|[0-9]|[a-zA-Z]", x)) >= 4) and (
                len(re.findall(r"", x)) == 3) and (len(re.findall(r"[a-zA-Z]", x)) == 0)) else 0

        homograph = lambda x: 1 if x.count("xn--") else 0

        forms = lambda x: 0 if len(x) == 0 else 1

        dicc1 = {"label":self.label, "url":self.url,"url.len": url(urlw.url), "url.domain.len": domains(urlw.domain),
                                     "url.homograph": homograph(urlw.domain), "url.subdomain.len": subdomains(urlw.subdomain),
                                     "url.tld.nores": tlds(urlw.domain), "url.tld.res": tlds2(urlw.domain),
                                     "url.tld.spons": tlds3(urlw.domain), "url.tld.countr": tlds4(urlw.domain),
                                     "url.special.chrtrs": pathschar(urlw.path),"url.verify.ip": verifyip(urlw.subdomain + urlw.domain),
                                     "url.paths.len": paths(urlw.path),"url.points": Counter(self.url)['.']}
        try:
            dicc1.update({'html description': forms(domain.formularios()["forms"])})
        except:
            dicc1.update({'html description': 0})

        dicc1.update({"have_ssl": extract_characteristics.ssl_issuer(certificate)[0],
                      "ssl_issuer": extract_characteristics.ssl_issuer(certificate)[-1],
                      "whois.ftr0": ((extract_characteristics.whois_characteristics(parse_response.jsonparser(data=data['w'], dict={}, keyword='Domain Whois Record'))[0])*2)+extract_characteristics.whois_characteristics(parse_response.jsonparser(data=data['w'], dict={}, keyword='Domain Whois Record'))[1]})
        dicc = parse_response.jsonparser(data=data['w'], dict={}, keyword='Domain Whois Record')
        dicc.update({'Registrar Whois Record': parse_response.jsonparser(data=data['w_server'], dict={}, keyword='')})

        html_charac = html_characteristics.compare_dom_whois(self.url, dicc)
        dicc1.update({'Domain_into_html': html_charac[0], 'whois_Comparation': html_charac[-1]})

        return dicc1










from threading import Thread, Event
import time


# Event object used to send signals from one thread to another
stop_event = Event()


def do_actions():
    """
    Function that should timeout after 5 seconds. It simply prints a number and waits 1 second.
    :return:
    """
    i = 0
    while True:
        i += 1
        print(i)
        time.sleep(1)

        # Here we make the check if the other thread sent a signal to stop execution.
        if stop_event.is_set():
            break








