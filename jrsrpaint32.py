#!/usr/bin/python
# -*- coding: utf-8 -*-
# License: 3-clause BSD License
# Author:  Rainbow
# Read-more: None
__author__ = 'Rainbow'

import psycopg2
import networkx as nx
import matplotlib.pyplot as plt



def clearallspace(text):
    return ''.join((text.strip()).split())

def getjrsrnum():
    return clearallspace(raw_input('Please type a "JRSRXXXX",just one.: ')).upper()

def selectcent(jrsrnum):
    return "select 本端局名称,对端局名称,光缆分类 from jrsrmodelreturn_201603_1 WHERE (传输环名称 = '" + jrsrnum +"') ORDER BY 传输环名称;"
    #return "select 本端局名称,对端局名称 from jrsrmodelreturn_201603 WHERE 传输环名称 = '" + jrsrnum +"' ORDER BY 传输环名称;"
    #return "select 本端局名称,对端局名称 from jrsrmodelreturn_201603 WHERE (备注 is null) and (传输环名称 = '" + jrsrnum +"') ORDER BY 传输环名称;"
    #return "select '('" + "||本端局名称||'" + "," +"'||对端局名称||')' from jrsrmodelreturn_201603 WHERE (备注 is null) and (传输环名称 = '" + jrsrnum +"') ORDER BY 传输环名称;"

def getdatafromdb(sentence):
    dbname = "kxyjya"
    username = "postgres"
    passwd = "000000"
    hostip = "127.0.0.1"
    portnum = "5432"
    print 'Now, connecting database, please wating......',
    connecter = psycopg2.connect(database=dbname, user=username, password=passwd, host=hostip,port=portnum)
    if connecter.status == 1:
        print ' Database connected!',
    else:
        print ' and Wating......'
    cur = connecter.cursor()
    cur.execute(sentence.decode(porstgresqldb))
    rows = cur.fetchall()
    connecter.close()
    print '...... Data be got from Database.'
    return rows

def jrsrnodepeer(dblist):
    peer = []
    #colornode = []
    #coloredge = []
    colornodeset = set()
    coloredgeset = set()
    for i in dblist:
        t=(i[0].decode(win732),i[1].decode(win732))
        #print i[2]
        if i[2] == u'中继光缆'.encode(win732): #== r'中继光缆': # != None:
            colornodeset.add(i[0].decode(win732))
            colornodeset.add(i[1].decode(win732))
            coloredgeset.add(t)
        peer.append(t)
    #print peer
    #print colornodeset
    #print coloredgeset
    return peer,colornodeset,coloredgeset

    '''
    peer = []
    for i in dblist:
        #peer.append(i)
        t=(i[0].decode(win732),i[1].decode(win732)) #WIN7 32, 特有。
        #t=(i[0],i[1])
        peer.append(t)
    return peer
    '''

def drawjrsr(jrsrpeers,jrsrnodes,jrsredges):
    usernodes = list()
    useredges = list()
    useredegestemp = set()
    JRSRG = nx.MultiGraph()
    JRSRG.add_edges_from(jrsrpeers)
    usernodes = list(set(JRSRG.nodes())-jrsrnodes)
    #for n in usernodes:
    #    print n,
    for ed in set(jrsrpeers):
        useredegestemp.add(ed)
    useredges = list(useredegestemp-jrsredges)

    #useredges = list(set(JRSRG.edges())-jrsredges)

    pos=nx.spring_layout(JRSRG)

    nx.draw_networkx_nodes(JRSRG,pos,list(jrsrnodes),node_color='g',node_size=3000,alpha=0.5,node_shape='s')
    nx.draw_networkx_nodes(JRSRG,pos,usernodes,node_color='y',node_size=1000,alpha=0.8)
    
    nx.draw_networkx_edges(JRSRG,pos,width=1.0,alpha=0.5)
    nx.draw_networkx_edges(JRSRG,pos,list(jrsredges),width=8,alpha=0.5,edge_color='r')
    nx.draw_networkx_edges(JRSRG,pos,useredges,width=8,alpha=0.4,edge_color='b')

    '''
    nx.draw_networkx_nodes(JRSRG,pos,node_color='g',node_shape='s',alpha=0.5,node_size=3000) # shape=>'o':圆,'s':方.
    nx.draw_networkx_edges(JRSRG,pos,alpha=0.5,width=6)
    '''
    nx.draw_networkx_labels(JRSRG,pos,font_size=15,font_family='sans-serif')

    #plt.title(jrsrname)
    #nx.draw(JRSRG)
    plt.show()



if __name__ == '__main__':
    win732 = 'GBK'
    win764 = 'utf-8'
    porstgresqldb = 'utf-8'

    jn = getjrsrnum()
    print jn
    seljncent = selectcent(jn)
    #print seljncent.decode('utf-8')
    jrsrnode = getdatafromdb(seljncent)
    jpeers,jnodes,jedges = jrsrnodepeer(jrsrnode)
    drawjrsr(jpeers,jnodes,jedges)



