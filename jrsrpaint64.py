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
    inputjrsrnum = raw_input('Please type a "JRSRXXXX",just one.: ')
    cjrsrnum = clearallspace(inputjrsrnum)
    #print cjrsrnum.upper()
    return cjrsrnum.upper()

def selectcent(jrsrnum):
    return "select 本端局名称,对端局名称,光缆分类 from jrsrmodelreturn_201603 WHERE (备注 is null) and (传输环名称 = '" + jrsrnum +"') ORDER BY 传输环名称;"
    #return "select 本端局名称,对端局名称,光缆分类 from jrsrmodelreturn_201603 WHERE (备注 is null) and (传输环名称 = '" + jrsrnum +"') ORDER BY 传输环名称;"
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
    cur.execute(sentence)
    rows = cur.fetchall()
    connecter.close()
    print '...... Data be got from Database.'
    return rows

def jrsrnodepeer(dblist):
    #import unicodedata
    peer = []
    #colornode = []
    #coloredge = []
    colornodeset = set()
    coloredgeset = set()
    for i in dblist:
        t=(i[0].decode(postgresql),i[1].decode(postgresql))
        #print i[2]
        if i[2] == u'中继光缆'.encode(win764doc): #== r'中继光缆': # != None:
            colornodeset.add(i[0].decode(postgresql))
            colornodeset.add(i[1].decode(postgresql))
            coloredgeset.add(t)
        peer.append(t)
    

        '''
        #peer.append(i)
        print 'Getdata from DB.',
        print i[0],i[1]
        t=(i[0].decode('utf-8'),i[1].decode('utf-8'))
        print 'Getdata from decode with utf-8.',
        print i[0].decode('utf-8'),i[1].decode('utf-8')
        print 'Getdata from encode with GBK.',
        print i[0].decode('utf-8').encode('GBK'),i[1].decode('utf-8').encode('GBK')
        #a = i[0].decode('utf-8').encode('GBK')
        #b = i[1].decode('utf-8').encode('GBK')
        #t = (a,b)
        #t=(i[0].decode('utf-8').encode('GBK'),i[1].decode('utf-8').encode('GBK'))
        #t = (unicodedata.normalize('NFC',i[0]),unicodedata.normalize('NFC',i[1]))
        #t=(i[0].encode('utf-8'),i[1].encode('utf-8'))
        peer.append(t)
        '''
    '''
    for n in colornodeset:
        colornode.append(n)

    for m in coloredgeset:
        coloredge.append(m)

    return peer,colornode,coloredge
    '''
    return peer,colornodeset,coloredgeset

def drawjrsr(jrsrpeers,jrsrnodes,jrsredges):
    usernodes = list()
    useredges = list()
    JRSRG = nx.Graph()
    JRSRG.add_edges_from(jrsrpeers)
    usernodes = list(set(JRSRG.nodes())-jrsrnodes)
    useredges = list(set(JRSRG.edges())-jrsredges)
    pos=nx.spring_layout(JRSRG)
    
    nx.draw_networkx_nodes(JRSRG,pos,list(jrsrnodes),node_color='r',node_size=600,alpha=0.8)
    nx.draw_networkx_nodes(JRSRG,pos,usernodes,node_color='b',node_size=300,alpha=0.8)
    
    nx.draw_networkx_edges(JRSRG,pos,width=1.0,alpha=0.5)
    nx.draw_networkx_edges(JRSRG,pos,list(jrsredges),width=8,alpha=0.5,edge_color='r')
    nx.draw_networkx_edges(JRSRG,pos,useredges,width=8,alpha=0.5,edge_color='b')


    #nx.draw_networkx_nodes(JRSRG,pos,node_color='g',alpha=0.5,node_size=5000)
    #nx.draw_networkx_edges(JRSRG,pos,width=6)
    nx.draw_networkx_labels(JRSRG,pos, font_size=15,font_family='sans-serif')
    #nx.draw(JRSRG)
    plt.show()



if __name__ == '__main__':
    win764sys = 'GBK'
    win764doc = 'utf-8'
    postgresql = 'utf-8'

    jn = getjrsrnum()
    print jn
    seljncent = selectcent(jn)
    #print seljncent.decode('utf-8')
    jrsrnode = getdatafromdb(seljncent)
    jpeers,jnodes,jedges = jrsrnodepeer(jrsrnode)
    drawjrsr(jpeers,jnodes,jedges)




