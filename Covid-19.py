#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys


# In[2]:


get_ipython().system('{sys.executable} --version')


# # import necessary libraries

# In[3]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import init_notebook_mode, plot, iplot


# ## Load Data
# 
# #### This data will be renewed day by day

# In[4]:


data = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')
data.head()


# In[5]:


data.tail(10)


# In[6]:


data.info()


# In[7]:


data.describe()


# ## Visualiize the data with plotly

# In[8]:


fig = px.choropleth(data,locations='Country',locationmode='country names',color='Confirmed',animation_frame='Date')
fig.update_layout(title='Choropleth Map of Confirmed Cases -till today',template="plotly_dark")
fig.show()


# In[9]:


fig = px.choropleth(data,locations='Country',locationmode='country names',color='Confirmed',animation_frame='Date',scope='africa')
fig.update_layout(title='Choropleth Map of Confirmed Cases - Africa till today',template="plotly_dark")
fig.show()


# ## Spread over Time

# In[10]:


fig = px.scatter_geo(data,locations='Country',locationmode='country names',color='Confirmed',size='Confirmed',hover_name="Country",animation_frame='Date',title='Spread over Time')
fig.update(layout_coloraxis_showscale=True,layout_template="plotly_dark")
fig.show()


# In[11]:


fig = px.choropleth(data,locations='Country',locationmode='country names',color='Recovered',animation_frame='Date')
fig.update_layout(title='Choropleth Map of Recovered Cases -till today',template="plotly_dark")
fig.show()


# In[12]:


fig = px.scatter_geo(data,locations='Country',locationmode='country names',color='Recovered',size='Recovered',hover_name="Country",animation_frame='Date',title='Recovery over Time')
fig.update(layout_coloraxis_showscale=True,layout_template="plotly_dark")
fig.show()


# In[13]:


fig = px.choropleth(data,locations='Country',locationmode='country names',color='Deaths',animation_frame='Date')
fig.update_layout(title='Choropleth Map of Deaths -till today',template="plotly_dark")
fig.show()


# In[14]:


fig = px.scatter_geo(data,locations='Country',locationmode='country names',color='Deaths',size='Deaths',hover_name="Country",animation_frame='Date',title='Deaths over Time')
fig.update(layout_coloraxis_showscale=True,layout_template="plotly_dark")
fig.show()


# ## extract latitudes & longtidues of locations

# In[15]:


import geopy
from geopy.geocoders import Nominatim


# In[16]:


geolocator=Nominatim(user_agent="app")


# In[17]:


location = geolocator.geocode("Egypt")
print(location.latitude, location.longitude)


# In[18]:


# copy the data to make changing
df = data.copy()


# In[19]:


df


# In[20]:


df[df['Country']=='Egypt'].tail(10)


# In[21]:


# Know the maximum value 
df2=df.groupby(['Country'])[['Confirmed','Recovered','Deaths']].max().reset_index()


# In[22]:


df2


# In[23]:


df2[df2['Country']=='Egypt']


# In[24]:


lat_lon=[]
geolocator=Nominatim(user_agent="app")
for location in df2['Country']:
    location = geolocator.geocode(location)
    if location is None:
        lat_lon.append(np.nan)
    else:    
        geo=(location.latitude,location.longitude)
        lat_lon.append(geo)


# In[25]:


lat_lon


# In[26]:


df2['geo_loc']=lat_lon


# In[27]:


lat,lon=zip(*np.array(df2['geo_loc']))


# In[28]:


df2['lat']=lat
df2['lon']=lon


# In[29]:


df2


# In[30]:


df2.drop(['geo_loc'],axis=1,inplace=True)


# In[31]:


df2


# In[32]:


import folium


# In[33]:


folium.Map(zoom_start=2)


# In[34]:


# Create a map
m = folium.Map(location=[54, 15], tiles='openstreetmap',zoom_start=2)

# Add points to the map
for id,row in df2.iterrows():
    folium.Marker(location=[row['lat'],row['lon']], popup=row['Confirmed']).add_to(m)

# Display the map
m


# In[35]:


for id,row in df2.iterrows():
    folium.Marker(location=[row['lat'],row['lon']], popup=row['Recovered']).add_to(m)

# Display the map
m


# In[36]:


m = folium.Map(location=[54, 15], tiles='openstreetmap', zoom_start=2)

# Add points to the map
for idx, row in df2.iterrows():
    folium.Marker([row['lat'], row['lon']], popup=row['Deaths']).add_to(m)

# Display the map
m


# In[37]:


m = folium.Map(location=[54,15], tiles='cartodbpositron', zoom_start=2)

# Add points to the map
from folium.plugins import MarkerCluster
mc = MarkerCluster()
for idx, row in df2.iterrows():
    mc.add_child(folium.Marker([row['lat'], row['lon']],popup=row['Confirmed']))
m.add_child(mc)

# Display the map
m


# In[38]:


from folium.plugins import HeatMap


# In[39]:


df2


# In[40]:


# Create map with overall cases registered
m = folium.Map(location=[54,15], zoom_start=2)
HeatMap(data=df2[['lat', 'lon','Confirmed']], radius=15).add_to(m)

# Show the map
m


# In[ ]:




