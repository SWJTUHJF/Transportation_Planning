import time
from File_import import read_net_create_LINK_NODE, read_nod, SPP_LC, SPP_LS, SPP_GLC

##################################
# 设置网络名称，计算算法
##################################

NETWORK = 'sf'  # sf = SiousFall;cs = ChicagoSketch; chi=ChicagoRegional
##################################
# 调用函数
##################################
LINK, NODE, NODE_COUNT, LINK_COUNT = read_net_create_LINK_NODE(NETWORK)
read_nod(NETWORK, NODE, NODE_COUNT)


# 根据link list获取路径长度
def get_length(Astarsp):
    sum_length = 0
    for i in Astarsp:
        sum_length += i.length  # sum the link cost
    print('length = ', sum_length)


# test general lable correcting algorithm
def Test_SPP_GLC(o_id, d_id):
    Lc_node = []  # store node list between o_id and d_id
    shortestpath_link = []  # store link list between o_id and d_id
    shortestpath_p_list = SPP_GLC(o_id, NODE, LINK)  # call glc function to calculate the shortest path tree
    if shortestpath_p_list[o_id] == -1:  # check correctness
        pass
    else:
        print('shortestpath_p_list is wrong!')

    # identify the shortest path from destination node to origin node
    head_n = NODE[d_id]
    Lc_node.append(d_id)
    tail_n = shortestpath_p_list[d_id]  # get the predecessor
    while tail_n != -1:
        for l in head_n.l_in:
            if l.tail_node == tail_n.node_id:  # get the exact link by predecessor
                shortestpath_link.insert(0, l)
        head_n = tail_n
        Lc_node.append(tail_n.node_id)
        tail_n = shortestpath_p_list[head_n.node_id]
    Lc_node.reverse()
    return (shortestpath_link, Lc_node)


# test the lable correcting algorithm
def Test_SPP_LC(o_id, d_id):
    Lc_node = []  # store node list between o_id and d_id
    shortestpath_link = []  # store link list between o_id and d_id
    shortestpath_p_list = SPP_LC(o_id, NODE)  # call LC function to calculate the shortest path tree
    if shortestpath_p_list[o_id] == -1:
        pass
    else:
        print('shortestpath_p_list is wrong!')
    # identify the shortest path from destination node to origin node
    head_n = NODE[d_id]
    Lc_node.append(d_id)
    tail_n = shortestpath_p_list[d_id]  # get the predecessor
    while tail_n != -1:
        for l in head_n.l_in:
            if l.tail_node == tail_n.node_id:  # get the exact link by predecessor
                shortestpath_link.insert(0, l)
        head_n = tail_n
        Lc_node.append(tail_n.node_id)
        tail_n = shortestpath_p_list[head_n.node_id]  # get the predecessor
    Lc_node.reverse()
    return (shortestpath_link, Lc_node)


# test the lable setting algorithm
def Test_SPP_LS(o_id, d_id):
    Lc_node = []  # store node list between o_id and d_id
    shortestpath_link = []  # store link list between o_id and d_id
    shortestpath_p_list = SPP_LS(o_id, d_id, NODE, LINK)  # call LC function to calculate the shortest path tree
    if shortestpath_p_list[o_id] == -1:
        pass
    else:
        print('shortestpath_p_list is wrong!')

    # identify the shortest path from destination node to origin node
    head_n = NODE[d_id]
    Lc_node.append(d_id)
    tail_n = shortestpath_p_list[d_id]  # get the predecessor
    while tail_n != -1:
        for l in head_n.l_in:
            if l.tail_node == tail_n.node_id:  # get the exact link by predecessor
                shortestpath_link.insert(0, l)
        head_n = tail_n
        Lc_node.append(tail_n.node_id)
        tail_n = shortestpath_p_list[head_n.node_id]  # get the predecessor
    Lc_node.reverse()
    print(len(NODE),type(NODE))
    return (shortestpath_link, Lc_node)


# 程序入口函数
start = time.time()  # 程序开始运行时间
# Astarsp, Astarspnode = Test_SPP_GLC(1, 24)
Astarsp, Astarspnode = Test_SPP_LC(1, 24 )
# Astarsp, Astarspnode = Test_SPP_LS(1, 24 )
end = time.time()  # 程序结束运行时间
print('LC run time =', end - start)
print(Astarspnode)
get_length(Astarsp)
