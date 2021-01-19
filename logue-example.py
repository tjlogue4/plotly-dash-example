

#import libraries
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

from datetime import datetime as dt

import plotly.graph_objs as go


import os


#Secret enviorment variables/ keys/ excel file name

dflink = os.environ['DATA_FRAME'] 


GOOGLE_TRACKING = os.environ['GOOGLE_TRACKING']

#Main Dataset
df = pd.read_excel(dflink)

#Subdata set for time based injury frequency
hourdf = df.groupby(df['Date & Time'].dt.hour).sum()

#Dataset conly containing records of ems was called 
emsdf = df[df['Emergency Personnel Called'] == True]

Injury_Type =['Ankle','Band_Aid','Bicep','Blister','Breathing','Cardio',
                'Collision', 'Elbow','Eye','Fainting','Finger','Foot',
                'Forearm','Glute','Groin','Hamstring','Hand','Head','Hip',
                'Ice','Knee','Mouth','Neck','Nose','Quad','Seizure','Shin',
                 'Shoulder', 'Vomit', 'Wrist']

#injery options formatter for dropdown
options=[]
for i in Injury_Type:
    
    stuff = {'label': i, 'value': i}
    options.append(stuff)

#formater for school selection

schooloptions=[]
for i in range(1,6):
    stuff = {'label': f'School #{i}', 'value': f'School #{i}'} 
    schooloptions.append(stuff)

locations = df['Location Type'].unique().tolist()

#initial options when user first visits page
locopt = ['Climbing Wall', 'Court - MAC', 'Court', 'Track','Pool', 
          'Field - Turf', 'Racquetball Court', 'Locker Room',
          'Group X Studio - MMA', 'Group X Studio', 'Field', 
          'Sand Volleyball Court', 'Bouldering', 'Fitness - Cardio', 
          'Fitness - Strength',  'Other']

locationopt =[]
for i in locations:
    stuff = {'label': i, 'value': i}
    locationopt.append(stuff)

    
activity = df['Activity Type'].unique().tolist()

#initial options when user first visits page
actopt = ['Adventures', ' Aquatics', 'Open Rec', 'Group Rental', 'Group X Class',
         'Intramurals', 'KHP Class', 'Other' ]

for i in activity:
    activityopt = []
    stuff = {'label': i, 'value': i}
    activityopt.append(stuff)
    
###
#time set up for displaying records at proper timestamp 
Time =  ['12:00 AM', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM',
         '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM',
         '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', 
         '9:00 PM', '10:00 PM', '11:00 PM']

index = []

for i in range(0,24):
    index.append(i)
    
merge = pd.DataFrame(data = pd.Series(0, index).reset_index())
merge.columns = ['Hour', 'Count']

###

#app =dash.Dash()

app = dash.Dash(__name__)
server = app.server

#style sheet stolen from the oil and gas example
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})


#if someone visits the page google analytics will work
if 'DYNO' in os.environ:
    app.scripts.append_script({
            'external_url': GOOGLE_TRACKING
                })

###
#layout

app.layout = html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P('Select a date range (between 11/04/2014 & 8/31/2017):'),                    
                                        dcc.DatePickerRange(
                                                            id='date_range',
                                                            min_date_allowed=dt(2014, 11, 4),
                                                            max_date_allowed=dt(2017, 8, 31),    
                                                            start_date=dt(2014, 11, 4),
                                                            end_date=dt(2017, 8, 31),
                                                            clearable = True,
                                                            reopen_calendar_on_clear=True,
                                                            ),
                                    ],
                                    className = 'three columns'
                                        ),
                                html.Div(
                                    [       
                                       html.P('Select what schools you would like to to be included:'),
                                       dcc.Checklist(
                                                     id='schools',
                                                     options =  schooloptions,
                                                     values = ['School #1', 'School #2', 'School #4'],
                                                     labelStyle={'display': 'inline-block'},
                                                     ),
                                    ],
                                    className = 'four columns',
                                        ),
                                html.Div(
                                    [
                                        html.P('Include Intramurals?'),
                                        dcc.RadioItems(
                                                       id='intraradio',
                                                       options =[
                                                        {'label': 'Yes', 'value': 'Yes'},
                                                        {'label': 'No', 'value': 'No'},
                                                                ],
                                                        value = 'Yes',
                                                        labelStyle={'display': 'inline-block'}
                                                        ),                
                                     ],
                                    className = 'two columns')
                            ],
                            className = 'row',
                                ),
        
                    html.Div(
                        [
                            html.Div(
                                [
                                        html.P('Select inury type(s):'),
                                        dcc.Dropdown(
                                                      id = 'injury_type',
                                                      options= options,
                                                      value=['Eye', 'Head', 'Mouth', 'Neck',
                                                               'Nose', 'Fainting', 'Collision', 'Shoulder'
                                                            ],
                                                      multi=True,
        
                                                      ),
                                ],
                                className = 'twelve columns'
                              ),
                             html.Div(
                                 [
                                        html.P('Select Location(s):'),
                                        dcc.Dropdown(
                                                     id='locinclude',
                                                     options = locationopt,
                                                     value = locopt,
                                                     multi = True,         
                                                    ),
                                ],
                                className = 'twelve columns'),
                        ],
                        className = 'row'),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Graph(id='c2bar'),
                                ],
                                className= 'five columns',
                                ),
                            html.Div(
                                [
                                    dcc.Graph(id = 'line'),
                                ],
                                className= 'seven columns',
                                    ),
                        ],
                        className='row',
                            ),
            
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Graph(id='count'),
                                ],
                                className= 'eight columns',
                                    ),
                            html.Div(
                                [
                                    dcc.Graph(id='pie'),
                                ],
                                className ='three columns'),
                        ],
                        className ='row',
                            ),                          
                     html.Div(
                         [
                            dcc.Graph(id='area'),

                          ],
                             ),
    
                    html.Div(
                        [
                            dcc.Graph(id='heat'),
                        ],
                            ),
                    ],
                        )

###
# dataframe updater


def update_df(df, schools, start_date, end_date, selector, activs):
    
    if selector == 'No':
        
        dff=df.loc[df['School #'].isin(schools)&
        (df['Activity Type'] != 'Intramurals')&
        (df['Location Type'].isin(activs))&
        ((df['Date & Time'] >= start_date)& 
        (df['Date & Time'] <= end_date))]
        return dff
    
    else:
        
        dff=df.loc[df['School #'].isin(schools)&
        (df['Location Type'].isin(activs))&
        ((df['Date & Time'] >= start_date)& 
        (df['Date & Time'] <= end_date))]
        return dff

###

###
# bar graph

@app.callback(
    dash.dependencies.Output('c2bar','figure'),
    [dash.dependencies.Input('schools', 'values'),
     dash.dependencies.Input('injury_type', 'value'),
    dash.dependencies.Input('date_range', 'start_date'),
    dash.dependencies.Input('date_range', 'end_date'),
    dash.dependencies.Input('locinclude', 'value'),
    dash.dependencies.Input('intraradio', 'value') 
    ]
)



def update_figure(schools, injury_type, start_date, end_date, activs, selector):

    dff = update_df(df, schools, start_date, end_date, selector, activs)

    x=injury_type
    y=[]
    
    for i in x:
        y.append(dff[i].sum())
        trace1all = go.Bar(x=x, y=y, name ='All')
        bars=[trace1all]
        
    return {
            'data': [trace1all],
            'layout': {
            'title':'Count by accident type in selection',
                       }
            }

###

# pie graph

@app.callback(dash.dependencies.Output('pie','figure'),
    [dash.dependencies.Input('schools', 'values'),
     dash.dependencies.Input('injury_type', 'value'),
     dash.dependencies.Input('date_range', 'start_date'),
    dash.dependencies.Input('date_range', 'end_date'),
    dash.dependencies.Input('locinclude', 'value'),
    dash.dependencies.Input('intraradio', 'value')
    ]
)



def update_figure(schools, injury_type, start_date, end_date, activs, selector):
    
    dff = update_df(df, schools, start_date, end_date, selector, activs)
    
    emsdf = dff[dff['Emergency Personnel Called'] == True]
    
    injtype=injury_type
    counts = []
    
    for i in injtype:
        stuff = emsdf[i].sum()
        counts.append(stuff)
        tracepie = go.Pie(labels=injury_type, values = counts , hole = 0.5)
    
    return {
        'data':[tracepie],
        'layout' :{
            'title':'Count of accidents that resulted in EMS'
                    }
            }

###

###
# line graph
        
@app.callback(dash.dependencies.Output('line','figure'),
    [dash.dependencies.Input('schools', 'values'),
     dash.dependencies.Input('c2bar', 'hoverData'),
     dash.dependencies.Input('date_range', 'start_date'),
     dash.dependencies.Input('date_range', 'end_date'),
     dash.dependencies.Input('locinclude', 'value'),
     dash.dependencies.Input('intraradio', 'value')
    ]
)



def update_figure(schools, hoverData, start_date, end_date, activs, selector):
    
    dff = update_df(df, schools, start_date, end_date, selector, activs)
    

    hourdf = dff.groupby(dff['Date & Time'].dt.hour).sum().reset_index()
    hourdf.rename(columns ={'Date & Time' : 'Hour'}, inplace = True)
    hourdf= pd.merge(merge, hourdf, how ='left', on='Hour')
  
    
    if not hoverData:
        word ='Eye'
    else:
        word =hoverData['points'][0]['x']
    hourplot = go.Scatter(x= Time, y = hourdf[word], 
                          mode = 'lines', line=dict(shape='spline'), connectgaps=True)
    
    return {
        'data': [hourplot],
        'layout' :{
            'title':f'{word} by hour, hover over graph to the left to change!'
                    }
            }

###

###
# heat graph            

@app.callback(
    dash.dependencies.Output('heat','figure'),
    [dash.dependencies.Input('schools', 'values'),
     dash.dependencies.Input('injury_type', 'value'),
    dash.dependencies.Input('date_range', 'start_date'),
    dash.dependencies.Input('date_range', 'end_date'),
    dash.dependencies.Input('locinclude', 'value'),
     dash.dependencies.Input('intraradio', 'value')
    ]
)



def update_figure(schools, injury_type, start_date, end_date, activs, selector):
   
    dff = update_df(df, schools, start_date, end_date, selector, activs)
    
    g = dff.groupby(['Location Type'])
    lt = sorted(dff['Location Type'].unique().tolist())
    
    z_array =[]
    
    for injury in injury_type:
        values = g[injury].count().tolist()
        #valsum = sum(values)/100
        #percent = [x / valsum for x in values]
        z_array.append(values)
    
    traceheat = go.Heatmap(z=z_array, x=lt, y = injury_type, 
                           zsmooth = 'fast', colorscale = 'Viridis',)
    
    return {
        'data' : [traceheat]
            }

###

###
# count graph           
    
@app.callback(
    dash.dependencies.Output('count','figure'),
    [dash.dependencies.Input('schools', 'values'),
     dash.dependencies.Input('injury_type', 'value'),
    dash.dependencies.Input('date_range', 'start_date'),
    dash.dependencies.Input('date_range', 'end_date'),
    dash.dependencies.Input('locinclude', 'value'),
     dash.dependencies.Input('intraradio', 'value')
    ]
)



def update_figure(schools, injury_type, start_date, end_date, activs, selector):
   
    dff = update_df(df, schools, start_date, end_date, selector, activs) 
    
 
    dflist =['Date & Time']
    
    for injury in injury_type:
        dflist.append(injury)
    
    
    dff = dff[dflist]

    dff=dff.dropna(axis = 0, how = 'all', subset = injury_type) 
    
     
    hourdf = pd.DataFrame(data=dff['Date & Time'].dt.hour.value_counts().reset_index())
    hourdf.columns = ['Hour', 'Count']
    hourdf =hourdf.sort_values(by = 'Hour')
    hourdf= pd.merge(merge, hourdf, how ='left', on='Hour').fillna('0')
    hourplot2school = go.Bar(x= Time, y = hourdf['Count_y'])
    
    return {
        'data' : [hourplot2school],
        'layout': {
            'title':'Count of all accidents in selction by hour'
                    }
            }


###

###
# area graph           

@app.callback(
    dash.dependencies.Output('area','figure'),
    [dash.dependencies.Input('schools', 'values'),
     dash.dependencies.Input('injury_type', 'value'),
    dash.dependencies.Input('date_range', 'start_date'),
    dash.dependencies.Input('date_range', 'end_date'),
    dash.dependencies.Input('locinclude', 'value'),
     dash.dependencies.Input('intraradio', 'value')
    ]
)


def update_figure(schools, injury_type, start_date, end_date, activs, selector):
   
    areas=[]
    
    dff = update_df(df, schools, start_date, end_date, selector, activs)
    
    dflist =['Date & Time']
    
    for injury in injury_type:
        dflist.append(injury)
 
    for school in schools:        
        
        dffl=dff[dff['School #'].str.contains(school)]
        dffl = dffl[dflist]
        dffl=dffl.dropna(axis = 0, how = 'all', subset = injury_type) 
       
        hourdf = pd.DataFrame(data=dffl['Date & Time'].dt.hour.value_counts().reset_index())
        hourdf.columns = ['Hour', 'Count']
        hourdf =hourdf.sort_values(by = 'Hour')
        hourdf= pd.merge(merge, hourdf, how ='left', on='Hour').fillna('0')
        trace1school = go.Scatter(
        x= Time, y = hourdf['Count_y'],
        fill='tozeroy', mode = 'none' ,name =f'{school}')

        areas.append(trace1school)
      
    return {
        'data' : areas,
        'layout': {
            'title':'Count of all accidents in selction by School'
                    }
            }


       


if __name__ == '__main__':
    app.run_server()