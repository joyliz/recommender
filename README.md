## Overview  📋
1. The web app is built using React.js for the front-end and python's  flask for the back-end.
2. It enable user to search and go through various details (like cast, genre, trailer, etc) 5000+ movies (all these details are fetched using an API by TMDB) .
3. Based on the searched movie users are recommended movie which are fetched for the python-flask backend that uses local dataset and content-based filtering algorithm for recommendation.
4. The web-app also allows user to get top movies filtered by genre (these are also fetched using an TMDB api) . 
5. The web app is responsive and can be used on mobile devies.  

----

## Installation 📦
1. Unzip to your local machine.
2.  Install all the libraries mentioned in the [requirements.txt] 
    ```shell
    $ pip install -r requirements.txt
    ```
 3. Then run the flask server by 
    ```shell
    $ python app.py
    ```
4. Go to the movie-recommender-app directory and install the node modules and build the project.
    ```shell
    $ cd movie-recommender-app
    $ npm install
    ```
5. Go to the package.json file and change the proxy to your flask server local port which is most likely localhost:5000
6. Then build the project by
    ```shell
    $ npm run build
    ```
7. To the local flask server to start the project
    > localhost :portNumber
    
9. **If this doesn't work** use 
    ```shell
    $ npm start
    ```
     
---
## Algorithm For Recommendation
The Recommendations are made by computing similarity scores for movies using consine simarity. For each movie tags are created by combining various details like genre of the movie, title, top cast, director and then they are converted to vectors using which similarity matrix is formed. Then for any searched movie the movies with the largest similarity score with it are sorted and then recommended.
### Cosine Similarity 



 ---
 ## References 
 1. TMDB's API : https://www.themoviedb.org/documentation/api
 2. Cosine Similarity : https://www.machinelearningplus.com/nlp/cosine-similarity/
