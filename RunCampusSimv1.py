# #############################################################################
#    RunCampusSim.py
#    August-September 2023
#    Michael E. Kress, Ph. D.
#    College of Staten Island, CUNY
#   
#    This code uses PySwmm as well as PySWMM_App, which is a front end of sorts to the 
#   command line version of SWMM
#   To run this code, first set the environment to PySWMM to load the required versions of Python and the associated libraries
#   Overall the objective is to do some parameter analysis pf the Campus SWMM Model
#   September 17, 2023
#   *  Major code clean-up and plotting reoutine.
#   *  Demonstrait 2 ways of retrieving resulta from the simulation: oner while running
#         the simulation and the second by reading the output file.
#   *  The section which uses the swmm_api is left as an example of using it; 
#         however, the parameter variation does not actually use it at this time.
#   *  The depth of both Culvert for the sensor and CulvertOne for the flow
#         from S2 independent from S5 and the Weir, which causes somewhat of an instability.
#         The weir needs fine tuning based on the ground truth and combined orifice weir
#         hydraulics.  Also, S5 needs some work to better understand and represent
#         the hydrology and what flows into the storm sewer network and whct
#         what goes overland to Loop Road and S2.
#
#
##########################################################################################
#
#!/usr/bin/env python
# coding: utf-8
# In[9]:
# -*- coding: utf-8 -*-
import os
#
#   For Pyswmm-api to read inp file
#
import csv
from decimal import Decimal, ROUND_DOWN
from tabulate import tabulate
import pandas as pd
import numpy as np
#
from swmm_api.input_file import read_inp_file, SwmmInput, section_labels as sections
from swmm_api.input_file.sections import Outfall
from swmm_api.input_file.macros.gis import write_geo_package, gpkg_to_swmm
#
#   Set the precision of the GIS variables in the configuration file 
from swmm_api import CONFIG
print(CONFIG)
CONFIG['gis_decimals'] = 10
print(CONFIG)
#
print(os.getcwd())
#WDirectory='C:\\Zhanyang\\SensorData\\CompoundFlooding\\SWMM\\PySWMM\\Campus\\Check'
WDirectory='C:\\Zhanyang\\SensorData\\CompoundFlooding\\SWMM\\PySWMM\\Campus\\S2S5Culverts\\Subcatchment2ParameterAnalysis\\WorkCampusPySwmm\\BaseV1'
#C:\Zhanyang\SensorData\CompoundFlooding\SWMM\PySWMM\Campus\S2S5Culverts\Subcatchment2ParameterAnalysis\WorkCampusPySwmm
os.chdir(WDirectory)
print(os.getcwd())
#
#   Read the inp file and print it to verify using swmm_api
#InputInpFile='AllCampus4_3V1a.inp'
InputInpFile='CampusS2S5CulvertWrStrParams.inp'
OutputInpFile='Out'+InputInpFile
print(InputInpFile)
print(OutputInpFile)
print(os.getcwd())
print(os.path.exists(InputInpFile))
inp = read_inp_file(InputInpFile)
print(inp)

# In[10]:
#
#   Next section run simulation with pyswmm
#
from pyswmm import Simulation, Subcatchments
#
import swmmio
#
with Simulation(r'./CampusS2S5CulvertWrStrParams.inp') as sim:
    #   Set up the parameters to be used for this run.
    S2 = Subcatchments(sim)["S2"]
    print('S2 Width =' +str(S2.width))
    #S2.width=400
    print('S2 Revised Width =' +str(S2.width))
    #
    #   Set up parameter information
    #
    for step in sim:
        print(sim.current_time)
        print(S2.runoff,S2.width)
        #   Tabulate interested variables


# In[11]:
import swmmio
#mymodel = swmmio.Model(r'C:\Zhanyang\SensorData\CompoundFlooding\SWMM\PySWMM\Campus\S2S5Culverts\Subcatchment2ParameterAnalysis\CampusS2S5CulvertWrStrParams.inp')
mymodel = swmmio.Model(r'./CampusS2S5CulvertWrStrParams.inp')
# Pandas dataframe with most useful data related to model nodes, conduits, and subcatchments
nodes = mymodel.nodes.dataframe
links = mymodel.links.dataframe
subs = mymodel.subcatchments.dataframe

#enjoy all the Pandas functions
#nodes.head()
from pyswmm import Simulation, Nodes, Links
with Simulation(r'CampusS2S5CulvertWrStrParams.inp') as sim:
    ########################
    # Simulation information
    # remaining references are available here:
    # https://pyswmm.readthedocs.io/en/stable/reference/simulation.html#pyswmm.simulation.Simulation
    print("Simulation info")
    flow_units = sim.flow_units
    print("Flow Units: {}".format(flow_units))
    system_units = sim.system_units
    print("System Units: {}".format(system_units))
    print("Start Time: {}".format(sim.start_time))
    print("Start Time: {}".format(sim.end_time))


# In[12]:
#
#
with Simulation(r'CampusS2S5CulvertWrStrParams.inp') as sim:
##################
    # Node Information
    # remaining references are available here:
    # https://pyswmm.readthedocs.io/en/stable/reference/nodes.html#pyswmm.nodes.Node
    NodeVJunction = Nodes(sim)["VJunction"]
    print("Node VJunction info")
    print("Invert Elevation: {}".format(NodeVJunction.invert_elevation))
    print("Physical Depth: {}".format(NodeVJunction.full_depth))
    print("Is it a Junction?: {}".format(NodeVJunction.is_junction()))

    ##################
    # Link Information
    # remaining references are available here:
    # https://pyswmm.readthedocs.io/en/stable/reference/links.html#pyswmm.links.Link
    LinkCulvert = Links(sim)['Culvert']
    LinkCulvertOne = Links(sim)['CulvertOne']
    print("Link Culvert info")
    print("Inlet Node ID: {}".format(LinkCulvert.inlet_node))
    print("Outlet Node ID: {}".format(LinkCulvert.outlet_node))

    # Launch a simulation!
    for ind, step in enumerate(sim):
        if ind % 100 == 0:
            print(sim.current_time,",",round(sim.percent_complete*100),"%",\
                  NodeVJunction.depth, LinkCulvert.flow)
    nodeVJunction_stat_out = NodeVJunction.statistics
    print(nodeVJunction_stat_out)
    print("Max Node VJunction Depth: {}".format(nodeVJunction_stat_out['max_depth']))
    linkCulvert_stat_out = LinkCulvert.conduit_statistics
    print("Link Culvert Peak Velocity: {}".format(linkCulvert_stat_out["peak_velocity"]))
    linkCulvert1_stat_out = LinkCulvertOne.conduit_statistics
    print("Link Culvert One Peak Velocity: {}".format(linkCulvert1_stat_out["peak_velocity"]))


# In[13]:
#
#   Get modules for plotting
#

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pyswmm import Simulation, Nodes, Links, Output
from swmm.toolkit.shared_enum import SubcatchAttribute, NodeAttribute, LinkAttribute


# In[7]:
#
#   Run parameters and plot variables and revise sizes of S2 or othe
#   parameters which are varied (note: not all parameters can be varied
#   some parameters will require changinf the *.inp file and rereading it 
#   for use in the simulation)
#
with Simulation(r'CampusS2S5CulvertWrStrParams.inp') as sim:
    NodeVJunction = Nodes(sim)["VJunction"]
    NodeCulvert1Out = Nodes(sim)["Culvert1Out"]
    NodeJWr1 = Nodes(sim)["JWr1"]
    LinkCulvert = Links(sim)['Culvert']
    LinkCulvertOne= Links(sim)['CulvertOne']
    LinkCulvertCon= Links(sim)['CulvertCon']
    LinkWeir1=Links(sim)['Weir1']
    S2 = Subcatchments(sim)["S2"]
    S5 = Subcatchments(sim)["S5"]
    print('S2 Width =' +str(S2.width)+' slope='+str(S2.slope)+' Area='+str(S2.area))
    #
    #   Set parameters to be revised here.
    #  
    #S2.area=204
    #S2.width=400
    #S2.width=1172
    #S2.slope=.005
    #S2.area=138.086
    #S2.width=276.
    #
    #   Cast as numbers to use in the title and file name because the type 
    #   in pyswmm did not cast to text correctly in matplot.
    #
    S2w=S2.width
    S2a=S2.area 
    S2slp=S2.slope 
    print('S2 Revised Width =' +str(S2.width)+' Revised Slope='+str(S2.slope)+'Revised Area='+str(S2.area))
    #
    #   Set the plot title
    #
    SCtitle=' Width=' +str(S2.width)+' Area='+str(S2.area)+' Slope='+str(S2.slope)
    print('SC'+SCtitle)
    #
    #   Set the plotfile name to encode parameter values.
    #
    PltFileName='S2'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    SensorFlDpthPltFileName='SenFlDpt'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    SensorMeasurePltFileName='SenMsrdFlDpt'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    CulDeptPltFileName='CulDept'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    WeirCCFlPltFileName='WeirCCFl'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    WeirJwrDpthPltFileName='WrJWrDpth'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    PltFileNameS2S5='S2S5Runoff'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    PltFileNameOne='S2CulvertOne'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    CulJwrFlowPltFileName='CulJwrFlow'+'W'+str(int(S2w))+'A'+str(int(S2a))+'Slpp'+str(round(S2slp*1000))+'.jpg'
    #
    # Initialize Lists for storing data for plotting and output
    #
    time_stamps = []
    node_head = []
    node_depth = []
    node_inflow = []
    node_outflow = []
    NodeJWr1_flow=[]
    NodeJWr1_depth=[]
    NodeCulvert1Out_flow=[]
    NodeCulvert1Out_depth=[]
    link_flow = []
    link_depth = []
    linkOne_depth = []
    LinkCulvertCon_flow=[]
    LinkWeir1_depth=[]
    LinkWeir1_flow=[]
    subc_runoff = []
    subc5_runoff=[]
    sim.step_advance(300)
    #
    # Launch a simulation!
    # This method of handeling the variables for plotting 
    # craetes lists of the output variables one at a time for each time step.
    #
    for ind, step in enumerate(sim):
        time_stamps.append(sim.current_time)
        node_head.append(NodeVJunction.head)
        node_depth.append(NodeVJunction.depth)
        node_inflow.append(NodeVJunction.total_inflow)
        node_outflow.append(NodeVJunction.total_outflow)
        NodeJWr1_flow.append(NodeJWr1.total_outflow)
        NodeJWr1_depth.append(NodeJWr1.depth)
        NodeCulvert1Out_flow.append(NodeCulvert1Out.total_outflow)
        NodeCulvert1Out_depth=[]
        link_flow.append(LinkCulvert.flow)
        link_depth.append(LinkCulvert.depth)
        linkOne_depth.append(LinkCulvertOne.depth)
        LinkCulvertCon_flow.append(LinkCulvertCon.flow)
        LinkWeir1_depth.append(LinkWeir1.depth)
        LinkWeir1_flow.append(LinkWeir1.flow)
        subc_runoff.append(S2.runoff)
        subc5_runoff.append(S5.runoff)
#
print(os.getcwd())
#
#   Write the Time and sensor simulated data to a csv file.
#
dfTime=pd.DataFrame(time_stamps)
#   add depth as a column
dfTime['depth']=link_depth
dfTime.to_csv('dfData.csv',index=False)
#
print("Read Uniform Interpolated Data after doing interpolation in Matlab")
dfSensorData = pd.read_csv ('UniformTimeDepth.csv')
print(dfSensorData)
#
#
#%%
#

# In[8]:
   
#
#   This method creates a dictionary from the sequence of tuples (time,value)
#   the Tuples are sorted and unpacked to plot get the values to plot.
#

with Output('CampusS2S5CulvertWrStrParams.out') as out:
    node_head_outfile = out.node_series('VJunction', NodeAttribute.HYDRAULIC_HEAD)
    link_flow_outfile = out.link_series('Culvert', LinkAttribute.FLOW_RATE)
    linkOne_depth_outfile = out.link_series('CulvertOne', LinkAttribute.FLOW_DEPTH)
    link_depth_outfile = out.link_series('Culvert', LinkAttribute.FLOW_DEPTH)
    LinkWeir1_depth_outfile = out.link_series('Weir1', LinkAttribute.FLOW_DEPTH)
    subc_runoff_outfile = out.subcatch_series('S2',SubcatchAttribute.RUNOFF_RATE)
print(link_depth_outfile)
#
for i in linkOne_depth_outfile:
    print (i) # this will print all keys
    print (linkOne_depth_outfile[i]) # this will print all values
lists2 = sorted(linkOne_depth_outfile.items()) # sorted by key, return a list of tuples
x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
#
lists1 = sorted(subc_runoff_outfile.items()) # sorted by key, return a list of tuples
x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples

#
# https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib.pyplot.figure
#
#%%
def PlotCompare(X1,Y1,Y2,PltTitle,X1Label,Y1Label,Y2Label,Legend1,Legend2,
                ShareYaxis,PltFile):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    fig = plt.figure(figsize=(8,4), dpi=200) #Inches Width, Height
    fig.suptitle(PltTitle)
    axis_1 = fig.add_subplot(2,1,1)
    axis_1.plot(X1, Y1, '-g' ,label=Legend1)
    axis_1.set_ylabel(Y1Label)
    axis_1.grid("xy")
    axis_1.legend()
    #
    #   Next do axis2
    #   Second Axis
    #
    if (ShareYaxis==1):
        axis_2 = fig.add_subplot(2,1,2, sharex=axis_1,sharey=axis_1)
    else:
        axis_2 = fig.add_subplot(2,1,2, sharex=axis_1)
    axis_2.plot(X1, Y2, color = 'g',label=Legend2)
    axis_2.set_ylabel(Y2Label)
    axis_2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %Hh'))
    axis_2.grid("xy")
    axis_2.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(PltFile)
    plt.show()
    #
    #    End PlotCompare.
    #
#
#   S2 runoff and Sensor depth
#
PlotCompare(X1=time_stamps,Y1=subc_runoff,Y2=link_depth,
            #PltTitle="S2 Runoff and Culvert One Depth"+SCtitle,
            PltTitle="S2 Runoff and Sensor Depth"+SCtitle,
            X1Label="Time",Y1Label="Flow (cfs)",Y2Label="Depth (ft)",
            Legend1="S2",Legend2="Sensor",ShareYaxis=0,PltFile=PltFileName)
#
#   Sensor Flow and Sensor depth
#
PlotCompare(X1=time_stamps,Y1=link_flow,Y2=link_depth,
            PltTitle="Sensor Flow and Sensor Depth"+SCtitle,
            X1Label="Time",Y1Label="Flow (cfs)",Y2Label="Depth (ft)",
            Legend1="Sensor Flow",Legend2="Sensor",ShareYaxis=0,PltFile=SensorFlDpthPltFileName)
#
#   Model Simulated Sensor Depth and Sensor Depth
# 
PlotCompare(X1=time_stamps,Y1=link_depth,Y2=dfSensorData.depth/12.0,
            PltTitle="Sensor Depth and Sensor Depth"+SCtitle ,
            X1Label="Time",Y1Label="Depth (ft)",Y2Label="Depth (ft)",
            Legend1="Simulated",Legend2="Mesured",ShareYaxis=0,PltFile="Test.jpg")
#
#    S2 and S5 flows.
#
PlotCompare(X1=time_stamps,Y1=subc_runoff,Y2=subc5_runoff,
            #PltTitle="S2 Runoff and Culvert One Depth"+SCtitle,
            PltTitle="S2 and S5 Runoff "+SCtitle,
            X1Label="Time",Y1Label="Flow (cfs)",Y2Label="Flow (cfs)",
            Legend1="S2",Legend2="S5",ShareYaxis=1,PltFile=PltFileNameS2S5)
#
#   Sensor (Culvert) and CulvertOne Depth 
#
PlotCompare(X1=time_stamps,Y1=linkOne_depth,Y2=link_depth,
            PltTitle="CulvertOne and Sensor Depth"+SCtitle,
            X1Label="Time",Y1Label="Depth (ft)",Y2Label="Depth (ft)",
            Legend1="CulvertOne",Legend2="Sensor",ShareYaxis=1,PltFile=CulDeptPltFileName)
#
#   Nodes Culvert1Out and JWr1 Flows
#
PlotCompare(X1=time_stamps,Y1=NodeCulvert1Out_flow,Y2=NodeJWr1_flow,
            PltTitle="Culvert1Out and JWr1 Flows "+SCtitle,
            X1Label="Time",Y1Label="Flow (cfs)",Y2Label="Flow (cfs)",
            Legend1="Culvert1Out",Legend2="JWr1",ShareYaxis=1,PltFile=CulJwrFlowPltFileName)
#
#   Weir Flow and CulvertCon Flow
#
PlotCompare(X1=time_stamps,Y2=LinkWeir1_flow,Y1=LinkCulvertCon_flow,
            PltTitle="CulvertCon and Weir1 Flow "+SCtitle,
            X1Label="Time",Y1Label="Flow (cfs)",Y2Label="Flow (cfs)",
            Legend2="Weir",Legend1="CulvertCon",ShareYaxis=1,PltFile=WeirCCFlPltFileName)
#
#   Weir Depth and JWr1 DEpth
#
PlotCompare(X1=time_stamps,Y2=LinkWeir1_depth,Y1=NodeJWr1_depth,
            PltTitle="JWr1 and Weir1 Depth "+SCtitle,
            X1Label="Time",Y1Label="Depth(ft)",Y2Label="Depth (ft)",
            Legend2="Weir",Legend1="JWr1",ShareYaxis=1,PltFile=WeirJwrDpthPltFileName)
#
#
##################
#
#   Next plot the dictionary variables and depth of CulvertOne
#
PlotCompare(X1=x1,Y1=y1,Y2=y2,
            PltTitle="S2 Runoff and Culvert One Depth"+SCtitle,
            #PltTitle="S2 Runoff and Sensor Depth"+SCtitle,
            X1Label="Time",Y1Label="Flow (cfs)",Y2Label="Depth (ft)",
            Legend1="S2",Legend2="Culvert One",ShareYaxis=0,PltFile=PltFileNameOne)
    
    

# In[9]:
#
#   Plotting section 
#      Set up filename and labels, titles, etc. with run information.
#

fig = plt.figure(figsize=(8,4), dpi=200) #Inches Width, Height
#fig.suptitle("Node VJunction Head and Link Culvert Depth ")
# Plot from the results compiled during simulation time
#fig.suptitle("Subcatchment S2 Runoff and Culvert Depth ")
fig.suptitle("S2 Runoff and Culvert Depth "+SCtitle)
#fig.subtitle(SCtitle)
#fig.suptitle(St)
axis_1 = fig.add_subplot(2,1,1)
#axis_1.plot(time_stamps, node_head, '-g', label="Running Sim")
axis_1.plot(time_stamps, subc_runoff, '-g' ,label="S2 Runoff")
# Plot from the output file - not used at this time
x = node_head_outfile.keys()
y = [node_head_outfile[key] for key in node_head_outfile.keys()]
#print(y)
#axis_1.plot(x, y, ':b', label="Output File")
#axis_1.set_ylabel("Head (ft)")
axis_1.set_ylabel("Flow (cfs)")
#axis_1.get_xticklabels().set_visible(False) # turns off the labels
axis_1.grid("xy")
axis_1.legend()
# Second Axis
axis_2 = fig.add_subplot(2,1,2, sharex=axis_1)
#axis_2.plot(time_stamps, link_flow, ls='-', color = 'g')
axis_2.plot(time_stamps, link_depth, color = 'g',label="Sensor")
#x = link_flow_outfile.keys()
#y = [link_flow_outfile[key] for key in link_flow_outfile.keys()]
x = link_depth_outfile.keys()
y = [link_depth_outfile[key] for key in link_flow_outfile.keys()]
#axis_2.plot(x, y, ':b', label="Output File")
axis_2.set_ylabel("Depth (ft)")
axis_2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %Hh'))
axis_2.grid("xy")
axis_2.legend()

#
# In[10]:

#FileName="S2W1172A535Slp5.jpg"
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("TEST.PNG")
fig.savefig(PltFileName)
plt.show()
#
#   Write current version of inp file.
#
inp.write_file(OutputInpFile)

print(str(link_depth))

# In[14]:


import swmmio

# Run Simulation PySWMM
with Simulation('./CampusS2S5CulvertWrStrParams.inp') as sim:
    for step in sim:
        pass

# Pass Give SWMM Simulation Artifacts to swmmio
crs = 'epsg:3728' # Coordinate Reference System
simulation_info = swmmio.Model("./CampusS2S5CulvertWrStrParams.inp", crs=crs)
#swmmio.create_map(simulation_info, filename="test.html")


# In[15]:


import swmmio
mymodel = swmmio.Model(r'./CampusS2S5CulvertWrStrParams.inp')

# Pandas dataframe with most useful data related to model nodes, conduits, and subcatchments
nodes = mymodel.nodes.dataframe
#links = mymodel.links.dataframe
subs = mymodel.subcatchments.dataframe

#enjoy all the Pandas functions
nodes.head()
subs.head()


# In[ ]:
from pyswmm import Simulation
import swmmio

# Run Simulation PySWMM
with Simulation(r'./CampusS2S5CulvertWrStrParams.inp') as sim:
    for step in sim:
        pass

# Pass Give SWMM Simulation Artifacts to swmmio
crs = 'epsg:3728' # Coordinate Reference System
simulation_info = swmmio.Model('./CampusS2S5CulvertWrStrParams.inp', crs=crs)
#   The following makes a conceptual model map but gives an error Skip for now.
#swmmio.create_map(simulation_info, filename='test.html')




# In[ ]:




