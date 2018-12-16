# Title
## Topics analysis of movies and TV series

# Abstract
Movies and TV Series are an integral part of lives of people all over the world. The themes that they engage in often reflect the social issues of the given time. In many cases they are the deciding factor of the film/tv series' popularity instead of its artistic merit. Is it possible to see how well the movie/tv series will be received based on its core themes? How big is the 'market' for movies/tv series tackling these social issues, compared to other topics? One of the social issues treated could be e.x. the Catholic church scandals in the previous years. We'll try to answer this question and others using the OpenSubtitles and IMDB databases.

# Research questions
* Are films/tv series that treat certain themes more likely to become box-office hits?
* Can we see any periodically-recurring themes in the subtitles?
* Are films/tv series that 'simpler' words and expressions more likely to be popular?
* How much influence does the film's location have on its success?

# Dataset
We're going to use the OpenSubtitles dataset and get the additional meta-data like the release date, box-office results and character names from IMDb. We'll have to apply some Natural Language Processing methods to filter out all the useless tokens (ponctuations tokens, adverbs, ...) form the subtitle XML files and match them with the IMDB movie/tv series ids. We'll detect the corresponding themes (therefore e.x. church) using arrays of words most commonly associated with the keyword and lematization.

Datasets:
* OpenSubtitles
* IMDB https://www.imdb.com/interfaces/


