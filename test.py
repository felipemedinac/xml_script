import xml.etree.ElementTree as ET
from hermetrics.hamming import Hamming
from hermetrics.osa import Osa
from tabulate import tabulate
import time

################Variables##############
archivo = 'test2.xml'
tree = ET.parse(archivo)
root = tree.getroot()
URLS = []
PARAM = []
osa = Osa()
url_config1 = {} ###############diccionarios con la configuracion############################
url_config2 = {} ###############diccionarios con la configuracion############################

url1_comparison={}
url2_comparison={}

def get_uris(URLS):
    for uri in root.findall("urls"):
        for child in uri:
            url=child.attrib.get("name")
            URLS.append(url)

def config_diff1(url1):
    for uri in root.findall("urls"):
        for child in uri:
            url=child.attrib.get("name")
            if url1 == url:
                print(f"URL name ---------------------------------> {url}")
                for childurl in child:
                    url_config1[childurl.tag]=childurl.text
                    for chiildurl2 in childurl:
                        url_config1[chiildurl2.tag] = chiildurl2.text
                        for chiildurl3 in chiildurl2:
                            url_config1[chiildurl3.tag] = chiildurl3

def config_diff2(url2):
    for uri in root.findall("urls"):
        for child in uri:
            url=child.attrib.get("name")
            if url2 == url:
                print(f"URL name ---------------------------------> {url}")
                for childurl in child:
                    url_config2[childurl.tag] = childurl.text
                    for chiildurl2 in childurl:
                        url_config2[chiildurl2.tag] = chiildurl2.text
                        for chiildurl3 in chiildurl2:
                            url_config2[chiildurl3.tag] = chiildurl3

def find_similarities_url(lista):
    try:
        for i in lista:
            for x in range(len(lista)):
                if lista.index(i) != x:
                    similitud = osa.similarity(i, lista[x])
                    if i.startswith(lista[x]) and similitud > 0.20:
                        #############################variables internas#################################
                        lista_similitud = []
                        lista_rec = []
                        ################################################################################
                        lista_rec.append(i)
                        lista_rec.append(lista[x])
                        similitud = str(similitud * 100)
                        similitud = f"Porcentaje de similitud: {similitud}"
                        lista_rec.append(similitud)
                        lista_similitud.append(lista_rec)
                        url1 = i
                        url2 = lista[x]
                        ################################obtener los diccionarios con la configuracion completa##########
                        config_diff1(url1)
                        config_diff2(url2)
                        ################################################################################################
                        comparar_diccionarios(url_config1,url_config2, lista_similitud)
                        print(lista_similitud)
                        print(tabulate(lista_similitud, headers=["URL1", "URL2", "porcentaje"], tablefmt='fancy_grid'))
    except NameError as e:
        print(e)

def comparar_diccionarios(url_config1, url_config2, lista_similitud):
    lista_diferencias_URL1 = [0, 1]
    Not_configured="Not configured"
    keys = url_config1.keys() | url_config2.keys()
    print("Lista similitud==================================>", lista_similitud)
    for key in keys:
        try:
            if url_config1[key] != url_config2[key]:
                # al parecer durante la recursividad el diccionario aumenta su tamano, no borra previos registros
                ########################comparacion de keys en diccionarios######################################
                url1_comparison[key] = url_config1[key]
                url2_comparison[key] = url_config2[key]
                #################################################################################################
                dir = {key: url1_comparison[key]}
                dir2 = {key: url_config2[key]}
                #################################################################################################
                ##################################diccionarios a insertar########################################
                lista_diferencias_URL1[0]=dir
                lista_diferencias_URL1[1]=dir2
                print("lista a insertar =============>", lista_diferencias_URL1)
                lista_similitud.append(lista_diferencias_URL1)
                #print("Lista similitud despues del apend1===> ", lista_similitud)
        except:
            if key not in url_config1:
                print(f"valor no configurado en URL 1  {key}")
                url1_comparison[key] = Not_configured
                url2_comparison[key] = url_config2[key]
                dir = {key:url1_comparison[key]}
                dir2 = {key:url_config2[key]}
                lista_diferencias_URL1[0] = dir
                lista_diferencias_URL1[1] = dir2
                print("lista a insertar =============>", lista_diferencias_URL1)
                lista_similitud.append(lista_diferencias_URL1)
                #print("Lista similitud despues del apend2===> ", lista_similitud)

            if key not in url_config2:
                print(f"valor no configurado en URL 2  {key}")
                url2_comparison[key] = Not_configured
                url1_comparison[key] = url_config1[key]
                dir = {key: url1_comparison[key]}
                dir2 = {key: url_config2[key]}
                lista_diferencias_URL1[0] = dir
                lista_diferencias_URL1[1] = dir2
                print("lista a insertar =============>", lista_diferencias_URL1)
                lista_similitud.append(lista_diferencias_URL1)
                #print("Lista similitud despues del apend3===> ", lista_similitud)

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
            lista = [i for i in URLS if i is not None]
            find_similarities_url(lista)


        if option == "2":
            pass

        if option == "3":
            print("ok")
        else:
            print("Done")

    except NameError as e:
        print(e)
