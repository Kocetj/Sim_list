from xml.dom import minidom
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import networkx as nx



def zberiPodatkeIzXML(xml):
    dat = minidom.parse(xml)
    moznePotiAvta = {}

    for avto in dat.getElementsByTagName('vehicle'):
        id = avto.getAttribute('id')
        ime = math.floor(float(id))
        pot = avto.getElementsByTagName('route')[0].getAttribute('edges')
        ceste = [int(i) for i in pot.split() if i.isdigit()]

        if ime not in moznePotiAvta:
            moznePotiAvta[ime] = []   
        moznePotiAvta[ime].append(ceste)
    return moznePotiAvta

def zasedenostCest(tmp):
    zasedenost = {}
    for avto in tmp:
        for id in tmp[avto]:
            if id not in zasedenost:
                zasedenost[id] = 0
            zasedenost[id]+=1
    return zasedenost

def primerjajResitvi(tmp, resitev):
    zasedenostTmp = list(zasedenostCest(tmp).values())
    zasedenostResitev = list(zasedenostCest(resitev).values())
    if np.std(zasedenostTmp) < np.std(zasedenostResitev):
        return True
    return False

def sestopanje(moznePotiAvtov, avto, tmp, resitev):    
    if avto > len(moznePotiAvtov):
        if not resitev:
            resitev.update(tmp)
        elif primerjajResitvi(tmp, resitev):
            resitev.update(tmp) 
        return 

    for pot in moznePotiAvtov[avto]:
        tmp[avto] = pot
        sestopanje(moznePotiAvtov, avto + 1, tmp, resitev)
        tmp[avto] = None

def izberiPoti(moznePotiAvtov):
    resitev = {}
    sestopanje(moznePotiAvtov, 1, {}, resitev)
    return resitev

#samo za prikaz
def zberiPodatkeZaGraf(xml1, xml2):
    dat1 = minidom.parse(xml1)
    dat2 = minidom.parse(xml2)

    vozlisca = {}
    povezave = {}

    for node in dat1.getElementsByTagName('node'):
        id = node.getAttribute('id')
        x = node.getAttribute('x')
        y = node.getAttribute('y')
        vozlisca[id] = ([x, y])
    
    for edge in dat2.getElementsByTagName('edge'):
        id = edge.getAttribute('id')
        od = edge.getAttribute('from')
        do = edge.getAttribute('to')
        povezave[id] = ([od, do])

    return vozlisca, povezave

def ustvariGraf():
    vozlisca, povezave = zberiPodatkeZaGraf('sim_list.nod.xml', 'sim_list.edg.xml')
    G = nx.DiGraph()
    for node, (x, y) in vozlisca.items():
        G.add_node(node, pos=(float(x), float(y)))
    for edge, (od, do) in povezave.items():
        G.add_edge(od, do, id=edge)
    return G, vozlisca, povezave

def narisiGrafResitve(optimalnaPorazdelitev):
    G, vozlisca, povezave = ustvariGraf()

    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(8, 6))

    nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black', font_weight='bold')
    zasedenost=zasedenostCest(optimalnaPorazdelitev)
    labels = nx.get_edge_attributes(G, 'id')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    for avto in optimalnaPorazdelitev:
        pot = []
        st = 1
        potX = []
        potY = []
        for cesta in optimalnaPorazdelitev[avto]:
            if st == 1:
                potX.append(float(vozlisca[povezave[str(cesta)][0]][0])+ avto * 1.5)
                potX.append(float(vozlisca[povezave[str(cesta)][1]][0])+ avto * 1.5)
                potY.append(float(vozlisca[povezave[str(cesta)][0]][1])+ avto * 1.5)
                potY.append(float(vozlisca[povezave[str(cesta)][1]][1])+ avto * 1.5)
                st-=1
            else:
                potX.append(float(vozlisca[povezave[str(cesta)][1]][0]) + avto * 1.5)
                potY.append(float(vozlisca[povezave[str(cesta)][1]][1]) + avto * 1.5)
        plt.plot(potX, potY)
    plt.axis('off')
    plt.show()


moznePotiAvtov = zberiPodatkeIzXML('sim_list.rou.xml')
optimalnaPorazdelitev = izberiPoti(moznePotiAvtov)
print(moznePotiAvtov)
print(optimalnaPorazdelitev)
print(zasedenostCest(optimalnaPorazdelitev))

narisiGrafResitve(optimalnaPorazdelitev)

