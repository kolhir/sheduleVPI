import requests
from bs4 import BeautifulSoup


urls = {
"ВТПЭ":"http://www.volpi.ru/vtpe/vtpe_membership/",
"ВИТ":"http://www.volpi.ru/vit/vit_membership/",
"ВЭМ":"http://www.volpi.ru/vem/vem_membership/",
"ВСГ":"http://www.volpi.ru/vsg/vsg_membership/",
"ВКФ":"http://www.volpi.ru/vfk/vfk_membership/",
"ВАЭиВТ":"http://www.volpi.ru/vae/vae_membership/",
"ВХТО":"http://www.volpi.ru/vht/vht_membership/",
"ВПФМ":"http://www.volpi.ru/vpf/vpf_membership/",
"ВАТ":"http://www.volpi.ru/vat/vat_membership/",
"ВТО":"http://www.volpi.ru/vto/vto_membership/",
"ВКМ":"http://www.volpi.ru/vkm/vkm_membership/",
"ВСТПМ":"http://www.volpi.ru/vstpm/vstpm_membership/"
}

import re

for url in urls:
    # print( url)
    r = requests.get(urls[url])
    r.encoding = "cp1251"
    soup = BeautifulSoup(r.text, features="html.parser")
    sp = soup.findAll("span", {"class":"f18"})
    for elem in sp:
        if len(elem.findAll('a')) == 0:
            s = re.sub(r'\s+', ' ', elem.text.replace("\r\n", ""))
            # print("   ", s)
        else:
            s = re.sub(r'\s+', ' ', elem.findAll('a')[0].text.replace("\r\n", ""))
            # print("   ", s)
