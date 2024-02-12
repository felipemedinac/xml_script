import xml.etree.ElementTree as ET
from hermetrics.hamming import Hamming
from hermetrics.osa import Osa
from tabulate import tabulate

################Variables##############
archivo = 'test2.xml'
tree = ET.parse(archivo)
root = tree.getroot()
URLS = []
PARAM = []
osa = Osa()
url_config1 = {}
url_config2 = {}
url_config1_2 = {}
url_config2_2 = {}


def comparar_diccionarios(url_config1, url_config2):
    keys = url_config1.keys() | url_config2.keys()
    for key in keys:
        if url_config1[key] != url_config2[key]:
            val1=url_config1[key]
            val2=url_config2[key]

            print(key, ":", url_config1[key], "-----------", key, ":", url_config2[key])
            return key, val1, val2

def comparar_diccionarios2(url_config1_2, url_config2_2):
    print("comparando")
    keys = url_config1_2.keys() | url_config2_2.keys()
    for key_2 in keys:
        if url_config1_2[key_2] != url_config2_2[key_2]:
            val1_2=url_config1_2[key_2]
            val2_2=url_config2_2[key_2]
            print()
            return key_2, val1_2, val2_2

def get_uris(URLS):
    for uri in root.findall("urls"):
        for child in uri:
            url=child.attrib.get("name")
            URLS.append(url)

def get_params(PARAM):
    for Parameters in root.findall("parameters"):
        for child in Parameters:
            parameter=child.attrib.get("name")
            PARAM.append(parameter)

def find_similarities_url(lista):
    try:
        for i in lista:
            for x in range(len(lista)):
                if lista.index(i) != x:
                    similitud = osa.similarity(i, lista[x])
                    if i.startswith(lista[x]) and similitud > 0.10:
                        lista_similitud = []
                        lista_rec = []
                        lista_rec2 = []
                        lista_rec2_2 = []
                        lista_rec.append(i)
                        lista_rec.append(lista[x])#####################################
                        similitud = str(similitud * 100)
                        similitud = f"Porcentaje de similitud: {similitud}"
                        lista_rec.append(similitud)
                        lista_similitud.append(lista_rec)
                        url1 = i
                        url2 = lista[x]
                        #print(url1, "    ", url2)
                        config_diff1(url1)
                        config_diff2(url2)
                        #comparar_diccionarios(url_config1, url_config2)
                        key, val1, val2 = comparar_diccionarios(url_config1, url_config2)#########################
                        diff1=key,":",val1
                        diff2=key, ":", val2
                        lista_rec2.append(diff1)
                        lista_rec2.append(diff2)
                        lista_similitud.append(lista_rec2)

                        #key_2, val1_2, val2_2 = comparar_diccionarios(url_config1_2, url_config2_2)  ##################
                        #diff1_2 = key_2, ":", val1_2
                        #diff2_2 = key_2, ":", val2_2
                        #lista_rec2_2.append(diff1_2)
                        #lista_rec2_2.append(diff2_2)
                        #lista_similitud.append(lista_rec2_2)
                        print(lista_similitud)
                        print(tabulate(lista_similitud, headers=["URL1", "URL2", "Porcentaje"], tablefmt='fancy_grid'))
                        #comparar_diccionarios(url_config1, url_config2)

        #print(lista)
    except NameError as e:
        print(e)

def find_similarities_param():
    try:
        for i in lista2:
            for x in range(len(lista2)):
                if lista2.index(i) != x:
                    if i.startswith(lista2[x]):
                        similitud = osa.similarity(i, lista2[x])
                        if similitud > 0.5:
                            lista_similitud = []
                            lista_rec = []
                            lista_rec.append(i)
                            lista_rec.append(lista2[x])
                            #similitud = osa.similarity(i, lista2[x])
                            similitud = str(similitud * 100)
                            similitud = f"Porcentaje de similitud: {similitud}"
                            lista_rec.append(similitud)
                            lista_similitud.append(lista_rec)
                            print(tabulate(lista_similitud, headers=["Param1", "Param2", "Porcentaje"], tablefmt='fancy_grid'))

    except NameError as e:
        print(e)


def config_diff1(url1):
    for uri in root.findall("urls"):
        for child in uri:
            url=child.attrib.get("name")
            if url1 == url:
                print(f"URL name ---------------------------------> {url}")
                for childurl in child:
                    url_config1[childurl.tag]=childurl.text
                    #print(childurl.tag, "==> ", childurl.text)
                    for chiildurl2 in childurl:
                        url_config1_2[chiildurl2.tag] = chiildurl2.text
                        #print("------------------->  ", chiildurl2.tag, chiildurl2.attrib, chiildurl2.text)
                        #for chiildurl3 in chiildurl2:
                            #print("------------------------------->", chiildurl3.tag, chiildurl3.text)
                            #for chiildurl4 in chiildurl3:
                                #print("------------------------------->", chiildurl4.tag, chiildurl4.text)
            else:
                #print("Not ok")
                pass


def config_diff2(url2):
    for uri in root.findall("urls"):
        for child in uri:
            url=child.attrib.get("name")
            if url2 == url:
                print(f"URL name ---------------------------------> {url}")
                for childurl in child:
                    url_config2[childurl.tag] = childurl.text

                    #print(childurl.tag, "=> ", childurl.text)
                    #for chiildurl2 in childurl:
                        #print("------->  ", chiildurl2.tag, chiildurl2.attrib, chiildurl2.text)
                        #for chiildurl3 in chiildurl2:
                            #print("----------------->  ", chiildurl3.tag, chiildurl3.attrib)
                            #for chiildurl4 in chiildurl3:
                                #print("--------------------------->  ", chiildurl4.tag, chiildurl4.attrib)
            else:
                #print("URL not found")
                pass

if __name__ == "__main__":
    try:
        print(""""
        Options
        1.-find duplicated Parameters and URLs
        2.-find configurations differences
        3.-exit
        """)
        option = input("introduce the Option number >> ")

        if option == "1":
            get_uris(URLS)
            #get_params(PARAM)
            lista = [i for i in URLS if i is not None]
            lista2 = [i for i in PARAM if i is not None]
            find_similarities_url(lista)
            #find_similarities_param()


        if option == "2":
            url1 = input("URL 1 a comparar >> ")
            url2 = input("URL 2 a comparar >> ")
            config_diff1(url1)
            #print(url_config1)
            config_diff2(url2)
            #print(url_config2)
            comparar_diccionarios(url_config1, url_config2)

        if option == "3":
            print("ok")
            #break
        else:
            print("please choose bettween the following options 1, 2, or 3")

    except NameError as e:
        print(e)