import pandas as pd
import requests
from bs4 import BeautifulSoup
from databaseconnector import dbconnect
import random
from lxml import html, etree

headers = {"Accept-Language": "en-US, en;q=0.5"}
# headers = {'User-Agent': 'Mozilla/5.0'}
# paste your url from idmb here
url = "https://www.imdb.com/search/title/?genres=adventure,thriller&start=251&explore=title_type,genres&ref_=adv_nxt"

# replace movie_type with the movie genre you are scrapping
movie_type = 'others'

get_content = requests.get(url, headers=headers)
soup = BeautifulSoup(get_content.text, "html.parser")

"""
initialize the variables for storing specific data from the
web-page
"""
title = []
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
image = []
story = []

# get all the divs containing movies

movie_divs = soup.find_all('div', class_='lister-item mode-advanced')

"""
iterate through the divs to get all the movie content
such as the title, duration, votes, genre etc..
"""
for movie_div in movie_divs:
    # get the movie title
    movie_name = movie_div.h3.a.text
    title.append(movie_name)

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
    try:
        mv = movie_votes[0].text
    except IndexError:
        # if there is an exception, generate a random value
        mv = random.randint(10253, 99999)
    votes.append(mv)

    # get the second content that contains the movie gross
    movie_gross = movie_votes[1].text if len(movie_votes) > 1 else random.randint(45, random.randint(67, 89))
    gross.append(movie_gross)

    # get the movie genre
    movie_genre = movie_div.find('span', class_='genre').text
    genre.append(movie_genre)

    # get the imdb rating
    try:
        movie_rating = float(movie_div.strong.text)
    except AttributeError:
        movie_rating = round(random.uniform(5, 9), 1)
        movie_rating = float(movie_rating)
    rating.append(movie_rating)

    # get the movie duration
    movie_duration = movie_div.find('span', class_='runtime').text if movie_div.p.find('span',
                                                                                       class_='runtime') else random.randint(
        90, 120)
    duration.append(movie_duration)

    # get the meta score
    movie_metascore = movie_div.find('span', class_='metascore').text if movie_div.find('span',
                                                                                        class_='metascore') else random.randint(
        24, 89)
    metascore.append(movie_metascore)

    # get the image
    image_src = movie_div.a.find('img', attrs={'class': 'loadlate'})
    image_tag = image_src.get("src")

    image.append(image_tag)

    movie_story = movie_div.find_all('p', class_='text-muted')[1].text
    story.append(movie_story)

"""
putting the data into a panda data frame
"""
movies = pd.DataFrame({
    'title': title,
    'movie_year': years,
    'movie_type': movie_type,
    'duration': duration,
    'rating': rating,
    'metascore': metascore,
    'votes': votes,
    'directorstars': director_stars,
    'gross': gross,
    'genre': genre,
    'story': story,
    'image': image
})

"""
cleaning the data;removing quotes
converting the data to the correct data types
"""
movies['movie_year'] = movies['movie_year'].str.extract('(\d+)').astype(int)
try:
    movies['duration'] = movies['duration'].str.extract('(\d+)').astype(int)
    movies['metascore'] = movies['metascore'].astype(int)
    movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
    movies['gross'] = movies['gross'].map(lambda x: x.lstrip('$').rstrip('M'))
    movies['gross'] = pd.to_numeric(movies['gross'], errors='coerce')
except (ValueError, AttributeError):
    movies['duration'] = duration
    movies['metascore'] = metascore
    movies['votes'] = rating
    movies['gross'] = gross

movies['image'] = movies['image'].str.replace(',', '')
movies['directorstars'] = movies['directorstars'].str.replace('\n', '')
movies['directorstars'] = movies['directorstars'].str.replace("|", "")
movies['genre'] = movies['genre'].str.replace('\n', '')
# movies['genre'] = movies['genre'].str.replace(',', '')
movies['story'] = movies['story'].str.replace('\n', '')

"""
saving the movies to database
"""
connection = dbconnect()
movies.to_sql(con=connection, name=movie_type)
print('data saved successfully to database')

"""
saving the data to specific files
remember to change the file name to you liking
"""

print('saving data...')
# save the data to a csv file
movies.to_csv('toprateds.csv')

# save the data to json(JSON FORMAT) file
json_file = movies.to_json()
with open('toprateds.json', 'a+') as file:
    file.write(json_file)

# save the data to TXT file
with open('toprateds.txt', 'a+') as file:
    file.write(json_file)
print('saved!')
