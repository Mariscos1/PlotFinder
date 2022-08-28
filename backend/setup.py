from bs4 import BeautifulSoup
import numpy as np

from tqdm import tqdm as prog_bar
import requests
import time
import wikipedia
import csv

# https://en.wikipedia.org/wiki/List_of_American_films_of_2022
def setup():

    title_link_year = set()
    for end_year in prog_bar(range(10, 23)):
        year = '20' + str(end_year)
        # print('year', year)
        html = requests.get('https://en.wikipedia.org/wiki/List_of_American_films_of_' + year)
        b = BeautifulSoup(html.text, 'lxml')
        
        for i in b.find_all(name='table', class_='wikitable'):
            for j in i.find_all(name='tr'):
                for k in j.find_all(name='i'):
                    for link in k.find_all('a', href=True):
                        # get the title and add to the list
                        title_link_year.add((link['title'], link['href'], year))
                        # print(link['title'])
        
        time.sleep(1)

    title_link_year

    possibles = ['Plot','Synopsis','Plot synopsis','Plot summary', 
                'Story','Plotline','The Beginning','Summary',
                'Content','Premise', 'Plot Summary']
                
    possibles_edit = [i + 'Edit' for i in possibles]
    #then merge those two lists together
    all_possibles = possibles + possibles_edit
    title_link_year = list(title_link_year)
    title_link_year.sort(key=lambda a: a[2])

    title_link_year


    f = open('temp_movie_corpus.csv', 'w')

    # create the csv writer
    writer = csv.writer(f)
    not_found = []
    for i in prog_bar(range(len(title_link_year))):
        title = title_link_year[i][0]
        year = title_link_year[i][2]
        wik = np.NaN
        try:
            wik = wikipedia.WikipediaPage(title)
        except:
            wik = np.NaN

    # a new try, except for the plot
        plot = np.NaN
        try:
            # for all possible titles in all_possibles list
            for j in all_possibles:
                # if that section does exist, i.e. it doesn't return 'None'
                if wik.section(j) != None:
                    #then that's what the plot is! Otherwise try the next one!
                    plot = wik.section(j).replace('\n','').replace("\'","")
                    break
        # if none of those work, or if the page didn't load from above, then plot
        # equals np.NaN
        except:
            plot= np.NaN
            
        if plot is np.NaN:
            not_found.append(i)
        else:
            data = [title, 'Movie', year, plot]
            writer.writerow(data)

    f.close()
    not_found 