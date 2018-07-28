'''
Created on Jul 25, 2018

@author: M1030512
'''

from bs4 import BeautifulSoup
from flask import Flask,jsonify
import os
import pandas as pd
from random import randint
import re
import requests
from time import sleep
from  urllib3 import *
import urllib3


app = Flask(__name__)
response_movie=None


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/imdb_data/movie',methods=['GET'])
def getAllMovie():
    return jsonify({'movies':response_movie})


class movie:  
   def __init__(self, name, yearOfRelease,plot,description,poster,rating,stars,directors,jonour):  
      self.name = name  
      self.yearOfRelease = yearOfRelease
      self.poster = poster
      self.plot = plot
      self.rating = rating
      self.stars=stars
      self.directors=directors
      self.description = description


def tranform_into_pandas(row_list):
    global response_movie
    movie_frame = pd.DataFrame(row_list,columns=['poster','name','desc','rating','directors','stars','movie_genre','yearOfRelease'] )
    print(movie_frame)
    resp = movie_frame.to_json(orient='records').replace("\\", "")
    print(resp)

def scrapePage(pageUrl):
    pass
    page=None
    proxy_set=True
    data =None
    proxy_url = "https://172.22.218.218:8085/"
#     directors=[]
#     movie_description = []
#     movie_genre=[]
#     movie_name = []  
#     movie_plot = []
#     movie_poster = []
#     movie_rating = []
#     movie_yearOfRelease = []
#     stars=[]
    
    records=[]
    
    for pages in range(1,4):
      
      try:
        default_headers = make_headers(proxy_basic_auth='M1030512:Mind@100')
#         http = ProxyManager(proxy_url, headers=default_headers)
        pageUrl = pageUrl+"&page="+ str(pages)
#         page = http.request('GET', pageUrl)
        if(proxy_set!=True):
          proxy = urllib3.ProxyManager(proxy_url,headers=default_headers)
          response = proxy.request('GET', pageUrl)
          data =response.data
        else:
          response = requests.get(pageUrl) 
          data =response.content 
      except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
      sleep(randint(1,4))
       
      soup = BeautifulSoup(data, 'html.parser')
#       html = list(soup.children)[3]
#       list(html.children)
        
      outer_list = soup.find(class_="lister-list")
      count =0
      movies_list = outer_list.find_all('div',class_="lister-item mode-advanced")
      print(len(movies_list))
       
      for movies in movies_list:
        row_list=[]
        row_content=""
        if movies.find('div', class_ = 'ratings-metascore') is not None:
          count=count+1
         
          movies_image_div = movies.find(class_="lister-item-image float-left")
          movies_image =movies_image_div.find("img")
          poster = movies_image['loadlate']
          str(poster).replace("\\\\", "/")
          row_list.append(str(poster).replace("\\\\", "/"))
          #row_content=row_content+poster
          #movie_poster.append(poster)
          #movie_name.append(poster)
          movies_content_div= movies.find(class_="lister-item-content")
          name= movies_content_div.find("a").get_text()
          #movie_name.append(name)
          #row_content=row_content+"|"+name
          row_list.append(name)
          
          desc = movies.find(class_="lister-item-content").find_all('p',class_="text-muted")[1].get_text()
          #row_content=row_content+"|"+desc
          #movie_description.append(desc)
          row_list.append(desc)
          rating_div = movies.find(class_="inline-block ratings-imdb-rating")
          if(rating_div!=None):
             rating = rating_div["data-value"]
             
          else:
              rating="NA"
          
          #movie_rating.append(rating)
          row_list.append(rating)
          #row_content=row_content+"|"+rating
         # starDesc=movies.find(class_="lister-item-content").find_next(class_="text-muted").get_text()
          
          star_Desc_Parent= movies.find(class_="lister-item-content").find(class_="sort-num_votes-visible")
          all_Cast=""
          list =[]
          if(star_Desc_Parent!=None):
              all_Cast=  star_Desc_Parent.find_previous_sibling()
          else:
              
              star_Desc_Parent = movies.find(class_="lister-item-content").find_all('p',class_="text-muted")[1]
              all_Cast = star_Desc_Parent.find_next()
              
          directors_tag =all_Cast.find_next() 
          while(directors_tag.get_text()!="|"):
                  pass
                  list.append(directors_tag.get_text())
                  directors_tag = directors_tag.find_next_sibling()
          starcast = ','.join(list)
          #srow_content=row_content+"|"+starcast
          
          #directors.append(starcast)
          row_list.append(starcast)
          list =None
          list = []
          while (directors_tag.find_next()!=None and directors_tag.find_next().parent.name=='p' and directors_tag.find_next().class_==None):
               list.append(directors_tag.find_next().get_text())
               directors_tag =directors_tag.find_next()
          director_Cast =','.join(list)  
          #row_content=row_content+"|"+director_Cast
          #stars.append(director_Cast)
          row_list.append(director_Cast)
          list= None  
          
          jonour=movies.find(class_="lister-item-content").find(class_="text-muted ").find(class_="genre").get_text()
          #movie_genre.append(jonour)
          #row_content=row_content+"|"+jonour
          row_list.append(jonour)
            
          yearOfRelease = movies_content_div.find(class_="lister-item-year text-muted unbold").get_text()
          #movie_yearOfRelease.append(yearOfRelease)
          #row_content=row_content+"|"+yearOfRelease
          row_list.append(yearOfRelease)
          records.append(row_list)
          
    tranform_into_pandas(records)
        
        
       
if __name__ == '__main__':
    pass 
    scrapePage("https://www.imdb.com/search/title?title_type=feature")
    #app.run()




