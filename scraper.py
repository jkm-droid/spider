import bs4 as bs4
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {"Accept-Language": "en-US, en;q=0.5"}

url = "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=drama&sort=user_rating," \
      "desc&start=51&ref_=adv_nxt "

get_content = requests.get(url, headers=headers)
soup = BeautifulSoup(get_content.text, "html.parser")

"""
initialize the variables for storing specific data from the
web-page
"""
titles = []
years = []
rating = []
metascore = []
director_stars = []
director = []
stars = []
votes = []
duration = []
genre = []
gross = []

# get all the divs containing movies

movie_divs = soup.find_all('div', class_='lister-item mode-advanced')

"""
iterate through the divs to get all the movie content
such as the title, duration, votes, genre etc..
"""
for movie_div in movie_divs:
    # get the movie title
    movie_name = movie_div.h3.a.text
    titles.append(movie_name)

    # get the release year
    movie_year = movie_div.h3.find('span', class_='lister-item-year')
    if movie_year is not None:
        yr = movie_year.text
        years.append(yr)
    else:
        yr = None
        years.append(yr)

    # get the movie director
    movie_director_stars = movie_div.find('p', class_='').text
    director_stars.append(movie_director_stars)

    # get the movie votes
    movie_votes = movie_div.find_all('span', attrs={'name': 'nv'})
    # get the first content that contains movie votes
    mv = movie_votes[0].text
    votes.append(mv)

    # get the second content that contains the movie gross
    movie_gross = movie_votes[1].text if len(movie_votes) > 1 else '0'
    gross.append(movie_gross)

    # get the movie genre
    movie_genre = movie_div.find('span', class_='genre').text
    genre.append(movie_genre)

    # get the imdb rating
    movie_rating = float(movie_div.strong.text)
    rating.append(movie_rating)

    # get the movie duration
    movie_duration = movie_div.find('span', class_='runtime').text if movie_div.p.find('span',
                                                                                       class_='runtime').text else '0'
    duration.append(movie_duration)

    # get the metascore
    movie_metascore = movie_div.find('span', class_='metascore').text if movie_div.find('span',
                                                                                        class_='metascore') else '0'
    metascore.append(movie_metascore)
"""
putting the data into a panda dataframe
"""
movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'duration': duration,
    'rating': rating,
    'metascore': metascore,
    'genre': genre,
    'votes': votes,
    'gross': gross,
    'directorstars': director_stars,
})
"""
cleaning the data;removing quotes
converting the data to the correct data types
"""
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['duration'] = movies['duration'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['gross'] = movies['gross'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['gross'] = pd.to_numeric(movies['gross'], errors='coerce')
movies['directorstars'] = movies['directorstars'].str.replace('\n', '')
movies['directorstars'] = movies['directorstars'].str.replace('|', '')
movies['genre'] = movies['genre'].str.replace('\n', '')
# movies['genre'] = movies['genre'].str.replace(',', '')

"""
saving the data to specific files
"""
json_file = movies.to_json()
print('Saving...')
with open('json.txt', 'a+') as file:
    file.write(json_file)
print('saved!')

print('saving csv')
movies.to_csv('movies1.csv')
print('saved!')
