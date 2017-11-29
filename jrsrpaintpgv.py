#!/usr/bin/python
# -*- coding: utf-8 -*-
# License: 3-clause BSD License
# Author:  Rainbow
# Read-more: None
__author__ = 'Rainbow'

import psycopg2
import networkx as nx
#from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt



def clearallspace(text):
    return ''.join((text.strip()).split())

def getjrsrnum():
    return clearallspace(raw_input('Please type a "JRSRXXXX",just one.: ')).upper()

def selectcent(tabname,jrsrnum):
    return "select 本端局名称,光缆分类,传输设备类型,光缆统一标识,纤号,对端局名称 from " + tabname + " WHERE (传输环名称 = '" + jrsrnum + "') ORDER BY 传输环名称;"
    #return "select 本端局名称,对端局名称,光缆分类 from jrsrmodelreturn_201603_1 WHERE (传输环名称 = '" + jrsrnum +"') ORDER BY 传输环名称;"
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
    #peer = []
    #colornode = []
    #coloredge = []
    #colornodeset = set()
    trunknodeset = set() #中继缆的两端都存这里
    #coloredgeset = set()
    trunkedgeset = list() #中继缆存这里，因为会遇到同局对间同缆的问题，列表内存储的是[((局点,局点),缆号),]
    devicenodeset = set() #左侧含有设备的节点存这里
    bridgenodeset = set() #过桥节点，包括用户侧过桥
    useredgeset = list() #用户缆的两端存这里。参看trunkedgeset说明。遗漏A/B向问题。
    usernodeset = set() #用户缆的两端存这里，肯定有局端，做集合减法就好。
    trunkcablelabeldict = dict() #中继光缆节点对的光缆编号，及颜色
    usercablelabeldict = dict()  #用户光缆节点对编号，颜色
    usernodetemp = set() #用户节点暂存，要减去局点才是用户节点。
    for i in dblist:
        #print i[2]
        if i[1] == u'中继光缆'.encode(win732): #== r'中继光缆': # != None:
            trunknodeset.add(i[0].decode(win732)) #局端节点
            trunknodeset.add(i[5].decode(win732)) #局端节点
            '''
            keyy = i[0].decode(win732) + u'--' + i[5].decode(win732)
            trunkcablelabeldict[keyy] = i[3] + '/' + i[4] #增加中继光缆字典关键字。
            '''
            #a = sorted([i[0].decode(win732),i[5].decode(win732)])
            t =(tuple(sorted([i[0].decode(win732),i[5].decode(win732)])),i[3])
            #print t
            trunkedgeset.append(t) #局间连接
        elif i[1] == u'用户光缆'.encode(win732):
            usernodetemp.add(i[0].decode(win732))
            usernodetemp.add(i[5].decode(win732))
            '''
            keyy = i[0].decode(win732) + u'--' + i[5].decode(win732)
            usercablelabeldict[keyy] = '' #i[4] + '/' + i[5] #增加用户光缆关键字。
            '''
            t =(tuple(sorted([i[0].decode(win732),i[5].decode(win732)])),i[3])
            #t=(i[0].decode(win732),i[5].decode(win732))
            useredgeset.append(t) #用户到局连接
        if i[2] is not None:
            devicenodeset.add(i[0].decode(win732))
        else:
            bridgenodeset.add(i[0].decode(win732)) #按左侧节点计算过桥点
            #bridgenodeset.add(i[5].decode(win732)) #按左侧节点计算过桥点，右侧节点不算了。
        #peer.append(t)
    
    for i in trunkedgeset:  #制作局点的中继字典
        keyy = i[0][0] + u'--' + i[0][1]
        if trunkcablelabeldict.has_key(keyy) is True:
            trunkcablelabeldict[keyy].append(i[1])     
        else:
            trunkcablelabeldict[keyy] = list()
            trunkcablelabeldict[keyy].append(i[1])
    
    for i in useredgeset:  #制作节点接入光缆字典
        keyy = i[0][0] + u'--' + i[0][1]
        if usercablelabeldict.has_key(keyy) is True:
            usercablelabeldict[keyy].append(i[1])
        else:
            usercablelabeldict[keyy] = list()
            usercablelabeldict[keyy].append(i[1])     

    usernodeset = usernodetemp - trunknodeset

    print ('trunknodeset: '),
    for i in trunknodeset:
        print i,
    print
    print ('trunkedgeset: '),
    for i in trunkedgeset:
        for n in i:
            if type(n) is tuple:
                for m in n:
                    print m,
            else:
                print n,
        print '|',
    print
    print ('devicenodeset: '),
    for i in devicenodeset:
        print i,
    print 
    print ('bridgenodeset: '),
    for i in bridgenodeset:
        print i,
    print
    print ('useredgeset: '),
    for i in useredgeset:
        for n in i:
            if type(n) is tuple:
                for m in n:
                    print m,
            else:
                print n,
        print '|',
    print
    print ('trunkcablelabeldict: '),
    for i in trunkcablelabeldict:
        print i,trunkcablelabeldict[i],
    print
    print ('usercablelabeldict: '),
    for i in usercablelabeldict:
        print i,usercablelabeldict[i],
    print
    print ('usernodeset: '),
    for i in usernodeset:
        print i,
    print
    #print peer
    #print colornodeset
    #print coloredgeset
    #return peer,trunknodeset,trunkedgeset,devicenodeset

    '''
    peer = []
    for i in dblist:
        #peer.append(i)
        t=(i[0].decode(win732),i[1].decode(win732)) #WIN7 32, 特有。
        #t=(i[0],i[1])
        peer.append(t)
    return peer
    '''
    return list(trunknodeset),trunkedgeset,list(devicenodeset),list(bridgenodeset),list(usernodeset),useredgeset,trunkcablelabeldict,usercablelabeldict

def drawjrsrpgv(jrsrnum,trunknode,trunkedge,devicenode,bridgenodes,usernode,useredge,trunkcablelabel,usercablelabel):
    import time
    import os
    import pygraphviz as pgv

    home = os.chdir(u'd:\\trunkcheckpngtemp')
    time = time.localtime()
    filetime = str(time[0]) + '-' + str(time[1]) + '-' +str(time[2]) + '-' +str(time[3]) + '-' +str(time[4]) + '-' +str(time[5])
    flname = filetime + '_' + jrsrnum

    G=pgv.AGraph()
    G=pgv.AGraph(strict=False,directed=True)
    G.graph_attr['center'] = True
    #G.graph_attr['rankdir'] = 'LR'
    G.graph_attr['bgcolor'] = "#FFF5EE"
    G.graph_attr['layout'] = 'circo'
    G.graph_attr['label'] = jrsrnum
    G.graph_attr['fontname'] = "Sans"
    G.graph_attr['lheight'] = 0.3
    G.graph_attr['dpi'] = 600
    G.edge_attr['dir']='none'
    G.node_attr['fontname'] = "Sans"
    #G.node_attr['fontname'] = "Miecrosoft YaHei"
    G.node_attr['fontsize'] = 12
    G.node_attr['fontcolor'] = 'black'

    #print trunknode
    G.add_nodes_from(trunknode)
    #print usernode
    G.add_nodes_from(usernode)
    #print trunkedge
    for ttp in trunkedge:
        tp = list(ttp[0])
        tad = tp[0]
        tbd = tp[1]
        G.add_edge(tad,tbd)
    #print useredge
    for etp in useredge:
        ep = list(etp[0])
        ead = ep[0]
        ebd = ep[1]
        G.add_edge(ead,ebd)

    for tn in trunknode:
        tnode = G.get_node(tn)
        tnode.attr['shape']='box'
        tnode.attr['color']='blue'
    for en in usernode:
        enode = G.get_node(en)
        enode.attr['shape']='doublecircle'
        enode.attr['color']='green'        

    #print trunkedge
    for te in trunkedge:
        #print te
        #print te[0][0],te[0][1],te[1]
        tedge = G.get_edge(te[0][0],te[0][1])
        tedge.attr['color']='blue'
        tedge.attr['lable']= te[1]
    print useredge
    for ue in useredge:
        print ue
        print ue[0][0],ue[0][1],ue[1]
        uedge = G.get_edge(ue[0][0],ue[0][1])
        uedge.attr['color']='green'
        if ue[1] is None:
            uedge.attr['lable']= 'None'
        else:
            uedge.attr['lable']= "'" + ue[1] + "'"
    
    print flname
    G.write(flname + '.' + 'dot')
    G.draw(flname + '.' + 'png',prog='circo')


def drawjrsr(jrsrpeers):
    usernodes = list()
    useredges = list()
    useredegestemp = set()
    JRSRG = nx.MultiGraph()
    JRSRG.add_edges_from(jrsrpeers) #所有节点和边都从这里进入图，对节点和边的操作是与节点和边为索引对应的。

    usernodes = list(set(JRSRG.nodes())-jrsrnodes) #分离出用户节点。这些工作可以在上一个数据库处理函数里完成。
    #for n in usernodes:
    #    print n,
    for ed in set(jrsrpeers):  #分离局与局间的连线和用户与局之间连线。
        useredegestemp.add(ed)
    useredges = list(useredegestemp-jrsredges)

    #useredges = list(set(JRSRG.edges())-jrsredges)

    pos=nx.spring_layout(JRSRG)

    nx.draw_networkx_nodes(JRSRG,pos,list(jrsrnodes),node_color='g',node_size=3000,alpha=0.5,node_shape='s') #操作局节点颜色和形状大小。shape=>'o':圆,'s':方。
    nx.draw_networkx_nodes(JRSRG,pos,usernodes,node_color='y',node_size=2000,alpha=1,node_shape='o') #操作用户节点颜色和形状大小。shape=>'o':圆,'s':方。
    nx.draw_networkx_nodes(JRSRG,pos,list(jrsrdevnodes),node_color='b',node_size=1000,alpha=0.5,node_shape='o') #在有设备的节点上加画节点颜色和大小。shape=>'o':圆,'s':方。

    nx.draw_networkx_edges(JRSRG,pos,width=1.0,alpha=0.5) #缺省画的细边。
    nx.draw_networkx_edges(JRSRG,pos,list(jrsredges),width=8,alpha=0.5,edge_color='r') #局间的边，加画红色。
    nx.draw_networkx_edges(JRSRG,pos,useredges,width=8,alpha=0.4,edge_color='b') #用户到局的边，加画蓝色。

    '''
    nx.draw_networkx_nodes(JRSRG,pos,node_color='g',node_shape='s',alpha=0.5,node_size=3000) # shape=>'o':圆,'s':方.
    nx.draw_networkx_edges(JRSRG,pos,alpha=0.5,width=6)
    '''
    #font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
    nx.draw_networkx_labels(JRSRG,pos,font_size=15,font_weight='bold',font_family='sans-serif')

    #plt.title(jrsrname)
    #nx.draw(JRSRG)
    plt.show()



if __name__ == '__main__':
    win732 = 'utf-8' #省事了,不调代码了。
    win764 = 'utf-8'
    porstgresqldb = 'utf-8'

    tname = 'jrsrmodelreturn_201603_2'
    print tname
    jn = getjrsrnum()
    print jn
    seljncent = selectcent(tname,jn)
    #print seljncent.decode('utf-8')
    jrsrnode = getdatafromdb(seljncent)
    a,b,c,d,e,f,g,h = jrsrnodepeer(jrsrnode)
    drawjrsrpgv(jn,a,b,c,d,e,f,g,h)
    #jpeers,jnodes,jedges,jdevices = jrsrnodepeer(jrsrnode)
    #drawjrsr(jpeers,jnodes,jedges,jdevices)



