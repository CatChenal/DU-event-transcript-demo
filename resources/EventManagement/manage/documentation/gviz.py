# coding: utf-8
import os
import graphviz as gv


def set_gv_envir():
    """ Ad-hoc fix to have Graphiz (v2.38) working on my system. 
    Note that in case the error ExecutableNotFound occurs, the path to 
    graphviz must be added to the PATH variable, e.g:
    > "FileNotFoundError: [WinError 2] The system cannot find the file specified" 
    > "ExecutableNotFound: 
       failed to execute ['dot', '-Tsvg'], make sure the Graphviz executables are
       on your systems' PATH"
    The above is not sufficient: the error occurred even though graphviz, dot and
    neato are all on my system path.
    Calling this function on failed `try` solved the problem. (?)
"""
    gviz = os.path.join(os.environ['PROGRAMFILES(X86)'], 'Graphviz2.38', 'bin')
    os.environ["PATH"] += os.pathsep + gviz
    cnd_gv = os.path.join(os.environ['CONDA_PREFIX'], 'Library', 'bin', 'graphviz')
    os.environ["PATH"] += os.pathsep + cnd_gv


def plot_bookmarks_struc(bkm_data, gv_title='graph', frmt='png', eng='dot'):
    """
    Parameters:
    -----------
    :param bkm_data: Chrome bookmarks (json)
    :param top_name: to filter bookmarks to correct level/key
    :param gv_title: the descriptive part of the graphviz (dot/.gv) filename
    :param frmt: output format
    
    """
    try:
        bkm_graph = gv.Digraph(engine=eng)
    except:
        set_gv_envir()
        
    g_name = gv_title + '.gv'
    bkm_graph = gv.Digraph(node_attr={'shape': 'rectangle',  'fixedsize': 'False'},
                       graph_attr={'splines': 'ortho'},
                       filename=g_name,
                       strict=False,
                       engine=eng)
        
    bkm_graph.attr(size='8,12')
    
    # Main node:
    top = 'Google Chrome Bookmarks structure'
    bkm_graph.node(name=top, color='blue')
    
    # Level_0
    L0_keys = list(bkm_data.keys())
    level_0 = gv.Digraph(name='First level keys',
                         node_attr={'shape': 'oval', 'color':'lightgrey'},
                         graph_attr={'style':'filled',
                                     'label':'Top keys'})
    # Add nodes to level_0
    n_root = "roots" #"'root': level containing the managed folders data."
    for k in L0_keys:
        n = "{}".format(str(k))
        if k == 'roots':
            level_0.node(n, color='red')
        else:
            level_0.node(n, color='grey')
        bkm_graph.edge(top, n, color='grey')
    
    # Level_1 
    L1_keys = list(bkm_data['roots'].keys())
    level_1 = gv.Digraph(name='roots',
                         node_attr={'shape': 'oval', 'color':'lightgrey'},
                         graph_attr={'style':'filled',
                                     'label':'Managed folders root'})
    # Add nodes to level_1
    n_other = "other: 'Other Bookmarks'"
    for k in L1_keys:
        n = "{}".format(str(k))
        if k == 'other':
            level_1.node(n, label=n_other, color='red')
        else:
            level_1.node(n)
        level_0.edge(n_root, n, color='grey')
    
    # Level_2
    L2_keys = list(bkm_data['roots']['other'].keys())        
    level_2 = gv.Digraph(name=bkm_data['roots']['other']['name'],
                         node_attr={'shape': 'oval', 'color':'lightgrey'},
                         graph_attr={'style':'filled'})
    # Add nodes to level_2
    for k in L2_keys:
        n = "{}".format(str(k))
        if n == 'children':
            level_2.node(n, color='red')
        else:
            level_2.node(n)
        level_1.edge('other', n, color='grey')
        
    # Level_3 to show keys are different for items and subfolders
    level_3 = gv.Digraph(name='items type',
                         node_attr={'shape': 'rectangle',  'fixedsize': 'False'})
    fcol = 'purple'
    ftype = "child is folder"
    level_3.node(ftype, color=fcol)
    level_2.edge('children', ftype, color=fcol, style='dashed')
    
    ucol = 'darkgreen'
    utype = "child is url"
    level_3.node(utype, color=ucol)
    level_2.edge('children', utype, color=ucol, style='dashed')
    
    # Level_3F
    L3_fld_keys = list(bkm_data['roots']['other']['children'][0].keys())
    for kk in L3_fld_keys:
        nn = "{}".format(kk)
        #bkm_graph.node(nn)
        level_3.edge(ftype, nn, color=fcol)
        
    #Level_3U
    L3_url_keys = list(bkm_data['roots']['other']['children'][10].keys())
    for kk in L3_url_keys:
        nn = "{}".format(kk)
        #bkm_graph.node(nn)
        level_3.edge(utype, nn, color=ucol)

    level_2.subgraph(level_3)
    level_1.subgraph(level_2)
    level_0.subgraph(level_1)
    bkm_graph.subgraph(level_0)

    # save src and display:
    fig_dir = os.path.abspath(os.path.join(os.curdir, 'figures'))
    dot =  bkm_graph.save(filename=g_name, directory=fig_dir) # adds the dot ext
    fname = os.path.join(fig_dir, g_name)
    png = gv.render(engine=eng, filepath=fname, format=frmt)

    return bkm_graph