# Title
### Social issues in films and tv series and their reception

# Abstract
Movies and TV Series are an integral part of lives of people all over the world. The themes that they engage in often reflect the social issues of the given time. In many cases they are the deciding factor of the film/tv series' popularity instead of its artistic merit. Is it possible to see how well the movie/tv series will be received based on its core themes? How big is the 'market' for movies/tv series tackling these social issues, compared to other topics? One of the social issues treated could be e.x. the Catholic church scandals in the previous years. We'll try to answer this question and others using the OpenSubtitles and IMDB databases.

# Research questions
* Are films/tv series that treat certain themes more likely to become box-office hits?
* Can we see any periodically-recurring themes in the subtitles?
* Are films/tv series that 'simpler' words and expressions more likely to be popular?
* Are certain names associated more with leading characters?
* How much influence does the film's location have on its success?

# Dataset
We're going to use the OpenSubtitles dataset and get the additional meta-data like the release date, box-office results and character names from IMDB. Additionally we'll need the Datamuse API for language statistics.  We'll have to filter out punctuation and stop words from the subtitle XML files and match them with the IMDB movie/tv series ids. We'll detect the corresponding themes (therefore e.x. the catholic church) using arrays of words most commonly associated with the keyword.

Datasets:
* OpenSubtitles
* IMDB https://www.imdb.com/interfaces/
* Datamuse API http://www.datamuse.com/api/)

# A list of internal milestones up until project milestone 2
* Until 15.11.2018 - Collect the data and do the aforementioned clean-up
* Until 25.11.2018 - Write the exhaustive plan of what to do for milestone 3

# A list of internal milestones up until project milestone 3
* Until 02.12.2018 - Decide on 3 big recent social issues to check
* Until 09.12.2018 - Do the proper calculations (theme presence, language complexity, leading character names, most common cities)
* Until 16.12.2018 - Prepare the full data story
* Until ~16.01.2018 - Design a beautiful, clean and readable poster

# Questions for TAs
