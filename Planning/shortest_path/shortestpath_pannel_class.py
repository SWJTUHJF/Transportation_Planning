import time
from shortestpath_obj_class import  read_net_create_LINK_NODE,read_nod,SPP_LC,SPP_LS,SPP_GLC
##################################
#设置网络名称，计算算法
##################################

NETWORK = 'cs'# sf = SiousFall;cs = ChicagoSketch; chi=ChicagoRegional
LINK, NODE, NODE_COUNT, LINK_COUNT = read_net_create_LINK_NODE(NETWORK)
read_nod(NETWORK, NODE, NODE_COUNT)

#根据link list获取路径长度
def get_length(Astarsp):
    sum_length = 0
    for i in Astarsp:
        sum_length += i.length #sum the link cost
    print('length = ',sum_length)

#test general lable correcting algorithm
def Test_SPP_GLC(o_id,d_id):
    Lc_node = [] # store node list between o_id and d_id
    shortestpath_link = []  # store link list between o_id and d_id
    shortestpath_p_list = SPP_GLC(o_id,NODE,LINK) # call glc function to calculate the shortest path tree
    if shortestpath_p_list[o_id] == -1: # check correctness
        pass
    else:
        print('shortestpath_p_list is wrong!')

    #identify the shortest path from destination node to origin node
    head_n = NODE[d_id]
    Lc_node.append(d_id)
    tail_n = shortestpath_p_list[d_id] #get the predecessor
    while tail_n != -1:
        for l in head_n.l_in:
            if l.tail_node == tail_n.node_id: #get the exact link by predecessor
                shortestpath_link.insert(0,l)
        head_n = tail_n
        Lc_node.append(tail_n.node_id)
        tail_n = shortestpath_p_list[head_n.node_id]
    Lc_node.reverse()
    print(shortestpath_link[1].liAnk_id)
    return (shortestpath_link,Lc_node)
    

    
#test the lable correcting algorithm
def Test_SPP_LC(o_id,d_id):
    Lc_node = [] # store node list between o_id and d_id
    shortestpath_link = []  # store link list between o_id and d_id
    shortestpath_p_list = SPP_LC(o_id,NODE)  # call LC function to calculate the shortest path tree
    if shortestpath_p_list[o_id] == -1:
        pass
    else:
        print('shortestpath_p_list is wrong!')

    # identify the shortest path from destination node to origin node
    head_n = NODE[d_id]
    Lc_node.append(d_id)
    tail_n = shortestpath_p_list[d_id] #get the predecessor
    while tail_n != -1:
        for l in head_n.l_in:
            if l.tail_node == tail_n.node_id:#get the exact link by predecessor
                shortestpath_link.insert(0,l)
        head_n = tail_n
        Lc_node.append(tail_n.node_id)
        tail_n = shortestpath_p_list[head_n.node_id] #get the predecessor
    Lc_node.reverse()
    print(shortestpath_link[1])
    return (shortestpath_link,Lc_node)

#test the lable setting algorithm
def Test_SPP_LS(o_id,d_id):
    Lc_node = [] # store node list between o_id and d_id
    shortestpath_link = []  # store link list between o_id and d_id
    shortestpath_p_list = SPP_LS(o_id,d_id,NODE)  # call LS function to calculate the shortest path tree
    if shortestpath_p_list[o_id] == -1:
        pass
    else:
        print('shortestpath_p_list is wrong!')

    # identify the shortest path from destination node to origin node
    head_n = NODE[d_id]
    Lc_node.append(d_id)
    tail_n = shortestpath_p_list[d_id] #get the predecessor
    while tail_n != -1:
        for l in head_n.l_in:
            if l.tail_node == tail_n.node_id:#get the exact link by predecessor
                shortestpath_link.insert(0,l)
        head_n = tail_n
        Lc_node.append(tail_n.node_id)
        tail_n = shortestpath_p_list[head_n.node_id] #get the predecessor
    Lc_node.reverse()
    return (shortestpath_link,Lc_node)

# alg = input("使用GLC,LC还是LS算法：")
print(f"选取的是{NETWORK}网络")
time1=list()
time2=list()
time3=list()
# 程序入口函数
for i in range(2,12):
    print(f"O-D对为1-{i}的情况：")
    start = time.time() #程序开始运行时间
    Astarsp, Astarspnode = Test_SPP_GLC(1, i)
    end = time.time() #程序结束运行时间
    print('LC run time = %.4f'%(end*10 - start*10))
    time1.append('%.4f'%(end*10 - start*10))
    print ("最短路径为：",Astarspnode)
    get_length(Astarsp)
    start = time.time() #程序开始运行时间
    Astarsp, Astarspnode = Test_SPP_LC(1, i)
    end = time.time() #程序结束运行时间
    print('LC run time = %.4f'%(end*10 - start*10))
    time2.append('%.4f'%(end*10 - start*10))
    print ("最短路径为：",Astarspnode)
    get_length(Astarsp)
    start = time.time() #程序开始运行时间
    Astarsp, Astarspnode = Test_SPP_LS(1, i)
    end = time.time() #程序结束运行时间
    print('LC run time = %.4f'%(end*10 - start*10))
    time3.append('%.4f'%(end*10 - start*10))
    print ("最短路径为：",Astarspnode)
    get_length(Astarsp)
print("t1:",time1)
print("t2:",time2)
print("t3:",time3)

od=list()
for i in range(2,12):
    od.append(f"o-d:1-{i}")
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.options import TitleOpts,LegendOpts,ToolboxOpts,AxisOpts,AxisTickOpts

c = (
    Bar({"theme": ThemeType.MACARONS})
    .add_xaxis(od)
    .add_yaxis("GLC算法", time1)
    .add_yaxis("LC算法", time2)
    .add_yaxis("LS算法", time3)
    .reversal_axis()
    .set_global_opts(
        title_opts= TitleOpts(title="不同算法运行cs网络部分o-d对所需时间", pos_left="center", pos_bottom="1%"),
        legend_opts=LegendOpts(is_show=True),
        toolbox_opts=ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(name="毫秒"),
        yaxis_opts=opts.AxisOpts(name="o-d对"),
    )
    .render("bar_base_dict_config.html")
)
