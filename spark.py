import pandas as pd
import numpy as np 

df = pd.read_csv('data.csv')

def get_director_id(s):
    s1 = s
    s2 = 'Person id:'
    start = s1.index(s2) + len(s2)
    if s1[start:start+7].isnumeric():
        return s1[start:start+7]
    else:
        return np.nan

def get_director_name(s):
    s1 = s
    s2 = 'name:_'
    s3 = '_>]'
    start = s1.index(s2) + len(s2)
    end = s1.index(s3)
    try:
        return s1[start:end]
    except:
        return np.nan
    
def find(s, ch):
    l = []
    i = s.find(ch)
    while i!= -1:
        l.append(i)
        i = s.find(ch,i+1)
    return l

def get_cast_ids(s):
    start = find(s, '<Person id:')
    end = find(s, '[http]')
    id_list = []
    for i in range(len(end)):
        id_list.append(s[start[i]+11:end[i]])
    return id_list

def get_cast_names(s):
    start = find(s, 'name:_')
    end = find(s, '_>')
    name_list = []
    for i in range(len(end)):
        name_list.append(s[start[i]+6:end[i]])
    return name_list

def get_budget(s):
    start = s.find('$')
    end = s.find(' ')
    return int(s[start+1:end].replace(',',''))

def apply_genre(s):
    s = s.replace('\'','').replace('[','').replace(']','').split(sep = ', ')
    return s

def get_date(s):
    day = s[0:2]
    month = s[3:6]
    year = s[7:11]
    return day, month, year

def get_country(s):
    start = find(s, '(')
    end = find(s, ')')
    return s[start[0]+1:end[0]]

def get_runtime(s):
    s2 = s[2:]
    s3 = s2[:len(s2)-2]
    return int(s3)

for i in df.index:
    s = df.loc[i,'director']
    try:
        df.loc[i,'director_name'] = get_director_name(s)
    except:
        df.loc[i,'director_name'] = np.nan
    try:
        df.loc[i,'director_id'] = get_director_id(s)
    except:
        df.loc[i,'director_name'] = np.nan
        
    s = df.loc[i,'cast']
    try:
        df.loc[i,'cast_names'] = [[get_cast_names(s)]]
    except:
        df.loc[i,'cast_names'] = np.nan
    try:
        df.loc[i,'cast_ids'] = [[get_cast_ids(s)]]
    except:
        df.loc[i,'cast_names'] = np.nan

for i in df.index:
    s = df.loc[i,'original_air_date']
    # print(s)
    try:
        df.loc[i,'country'] = get_country(s)
        d,m,y = get_date(s)
        df.loc[i,'day'] = d 
        df.loc[i,'month'] = m
        df.loc[i,'year'] = y
    except:
        df.loc[i,'country'] = np.nan
        df.loc[i,'day'] = np.nan
        df.loc[i,'month'] = np.nan
        df.loc[i,'year'] = np.nan

for i in df.index:
    try:
        s = df.loc[i, 'runtime']
        df.loc[i, 'runtime'] = get_runtime(s)
    except:
        s = np.nan

for i in df.index:
    try:
        s = df.loc[i, 'color_info']
        if "Black" in s:
            df.loc[i, 'color_info'] = "Black and White"
        if "Color" in s:
            df.loc[i, 'color_info'] = "Color"
    except:
        s = np.nan

for i in df.index:
    try:
        s = df.loc[i, 'sound_mix']
        if "Silent" in s:
            df.loc[i, 'sound_mix'] = "Silent"
        elif "Mono" in s:
            df.loc[i, 'sound_mix'] = "Mono"
        elif "Dolby" in s:
            df.loc[i, 'sound_mix'] = "Dolby"
        elif "DTS" in s:
            df.loc[i, 'sound_mix'] = "DTS"
        else:
            df.loc[i, 'sound_mix'] = "Others"
    except:
        s = np.nan

df = df[['title','year','rating','runtime','kind','color_info','sound_mix','director_name', 'genre','director_id', 'cast_names', 
         'cast_ids','votes','country','day','month']]
df.dropna(subset = ["rating"], inplace=True)
df.to_csv('preprocess_data.csv', index =False)