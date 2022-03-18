from main.com.appgate.swordpish.utils import url_parser
from collections import Counter
import re


class FeaturesProvider:
    def extractFeaturesFromUrl(self, url):
        urlw = url_parser.URL(url)
        url_length = lambda x: 0
        pathsfun = lambda x: False
        paths = lambda x: 0
        pathschar = lambda x: 1
        domains = lambda x: 0

        subdomains = lambda x: 0
        """Dominios gTLD no restringidos"""
        tld = []
        """Dominios gTLD restringidos"""
        tld2 = []
        """Dominios gTLD patrocinados"""
        tld3 = []
        """Dominios gTLD paises"""
        tld4 = []

        tlds = lambda x: 1 if x.rsplit('.')[-1] in str(tld) else 0

        tlds2 = lambda x: 1 if x.rsplit('.')[-1] in str(tld2) else 0
        tlds3 = lambda x: 1 if x.rsplit('.')[-1] in str(tld3) else 0
        tlds4 = lambda x: 1 if x.rsplit('.')[-1] in str(tld4) else 0
        verifyip = lambda x: 1 if ((len(re.findall(r"2[0-5][0-5]|1[0-9][0-9]|[0-9][0-9]|[0-9]|[a-zA-Z]", x)) >= 4) and (
            len(re.findall(r"\.", x)) == 3) and (len(re.findall(r"[a-zA-Z]", x)) == 0)) else 0

        homograph = lambda x: 1 if x.count("xn--") else 0
        return {"label": '0', "url.len": url_length(url), "url.domain.len": domains(urlw.domain),
                "url.homograph": homograph(urlw.domain), "url.subdomain.len": subdomains(urlw.subdomain),
                "url.tld.nores": tlds(urlw.domain), "url.tld.res": tlds2(urlw.domain),
                "url.tld.spons": tlds3(urlw.domain), "url.tld.countr": tlds4(urlw.domain),
                "url.special.chrtrs": pathschar(urlw.path), "url.verify.ip": verifyip(urlw.subdomain + urlw.domain),
                "url.paths.len": paths(urlw.path),
                "url.points": Counter(url)['.']
                }
