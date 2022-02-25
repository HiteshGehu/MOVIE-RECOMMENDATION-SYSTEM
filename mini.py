import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
df1= pd.read_csv("/Users/hitesh/Desktop/Final/MovieRecommendation-System/movies.csv")
print(df1.head())
df2 = pd.read_csv("/Users/hitesh/Desktop/Final/MovieRecommendation-System/credits.csv")
print(df2.head())
df2.rename(columns={"movie_id": "id"}, inplace=True)
df3 = pd.merge(df1, df2)
df3["release_date"] = df3["release_date"].fillna('0000')
emp = df3["release_date"]
length = (len(df3["release_date"]))
year = []
for i in range(0, length):
    string = df3["release_date"][i]
    x = string[0:4]
    year.append(int(x))
df3["release"] = year
c= df3["keywords"]
key = [] 
for value in c:
    val = json.loads(value)
    key.append([])
    for x in val:
        key[-1].append(x["name"]) 
df3["keyword"]=key
col = df3["genres"]
genre = []
list1 = []

for value in col:
    val = json.loads(value)
    genre.append([])
    for x in val:
        genre[-1].append(x["name"].lower())
        list1.append(x["name"].lower())
        
Genre = list(set(list1))

df3["Genres"] = genre
Genre = [val.lower() for val in Genre]
col = df3["production_companies"]
production = []
for value in col:
    val = json.loads(value)
    production.append([])
    for x in val:
        production[-1].append(x["name"])
df3["production"] = production
t = df3["cast"]
cast1 = []
for value in t:
    val = json.loads(value)
    cast1.append([])
    for x in val:
        cast1[-1].append(x["name"])
df3["m_cast"] = cast1
t1=[]
for i in range(0,length):
    t1.append([])
    for j in df3.iloc[i]["Genres"]:
        t1[-1].append(j)
    for k in df3.iloc[i]["keyword"]:
        t1[-1].append(k)
    for z in df3.iloc[i]["production"]:
        t1[-1].append(z)
    for n in df3.iloc[i]["m_cast"]:
        t1[-1].append(n)
df3["key"]=t1
temp=[]
for i in range(0,length):
    s=''
    for val in df3.iloc[i]["key"]:
        s=s+str(val)
        s=s+' '
    temp.append(s)
df3["key"]=temp    
print(df3.head())
print(df3.columns)
df3 = df3.drop(columns=['genres','budget', 'status', 'tagline', 'spoken_languages',
                             'production_companies', 'cast', 'release_date','title','keywords','crew'])
df3["key"]=df3["key"].fillna('')
li=[]
for i in range(0,length):
    li.append(i)
df3["sno"]=li
print(df3.head())
# plt.figure(figsize=(15, 25))
# df3['release'].value_counts().sort_index().plot(kind="barh")
# plt.xlabel("frequency")
# plt.ylabel("year")
# plt.title("Year v/s Frequency")
# plt.show()
#Observed value
max_year = 2017
min_year=1916
v = df3["vote_count"]
c1 = df3["vote_average"].mean()
r = df3["vote_average"]
m = df3["vote_count"].quantile(0.40)
df3["rating"] = ((r*v) + (c1*m))/(v+m)
movies = df3.sort_values("rating", ascending=False)
movies=movies.drop(columns=["sno"])
top1=df3.sort_values("popularity", ascending=False)
print(movies.head(n=5))
def _genre_(gen):
    count=0
    temp=[]
    temp1=[]
    if gen.lower() in Genre:
        for i in range(0, length):
            x = movies.iloc[i]["Genres"]
            if gen.lower() in x:
                count+=1
                temp.append(movies.iloc[i]["original_title"])
                temp1.append(movies.iloc[i]["rating"])
                if count==10:
                    break
    return temp,temp1

def release_date(year):
     if year < min_year or year > max_year:
         return [],[]
     count = 0
     temp=[]
     temp1=[]
     for i in range(0, length):
        if year == int(movies.iloc[i]["release"]):
            count += 1
            temp.append(movies.iloc[i]["original_title"])
            temp1.append(movies.iloc[i]["rating"])
            if count==10:
                break
     return temp,temp1

def _top_():
    temp=[]
    temp1=[]
    temp2=[]
    for x in range(0,10):
        t=[]
        temp.append(top1.iloc[x]["original_title"])
        temp1.append(top1.iloc[x]["rating"])
        t.append(top1.iloc[x]["Genres"])
        temp2.append(t)
    return temp,temp1,temp2
def _info_(Movie_Name):
     temp=[]
     for x in range(0,length):
         if(movies.iloc[x]["original_title"]==Movie_Name):
             temp.append(movies.iloc[x]["original_title"])
             temp.append(movies.iloc[x]["runtime"])
             temp.append(movies.iloc[x]["homepage"])
             temp.append(movies.iloc[x]["overview"])
             break
     return temp
def similar(name,index):
     found = 1
     for i in range(0,length):
        if(df3.iloc[i]["original_title"]==name):
            found = 0
            break
     if (found == 1):
      return [],[]   
     c=CountVectorizer()
     matrix=c.fit_transform(df3["key"])
     cos=cosine_similarity(matrix)
     for i in range(0,length):
        if(df3.iloc[i]["original_title"]==name):
            index=df3.iloc[i]["sno"]
            break
     same=list(enumerate(cos[index]))
     similar_movies=sorted(same,key=lambda x:x[1],reverse=True)
     z=0
     temp=[]
     temp1=[]
    #  temp2=[]
     for string in similar_movies:
        for j in range(0,length):
            if(df3.iloc[j]["sno"]==string[0]):
                    #  t=[]
                    temp.append(df3.iloc[j]["original_title"])
                    temp1.append(df3.iloc[j]["rating"])
                    #  t.append(df3.iloc[j]["Genres"])
                    #  temp2.append(t)
                    break
        z=z+1
        if z==6:
         return temp,temp1
def all_movies():
    temp=[]
    for i in range(0,length):
        temp.append(movies.iloc[i]['original_title'])
        temp.sort()
    return temp
