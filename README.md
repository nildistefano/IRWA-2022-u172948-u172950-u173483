# IRWA-2022-u172948-u172950-u173483

### Authors

- Pol Ayala: u173483
- Toni Carbonell: u172950
- Nil Distefano: u172948

# Table of contents
- **[Part 1: Text Processing](#part-1-text-processing)**
- **[Part 2: Indexing and Evaluation](#part-2-indexing-and-evaluation)**
- **[Part 3: Ranking](#part-3-ranking)**

## Part 1: Text Processing

### Before running

It is necessary to put the correct data in each of the input/output folders:

- **Input data**

  Contained in `./data/` by default. Should contain:

  - `tw_hurricane_data.json` or any similarly formatted tweet collection JSON file.
  - `tweet_document_ids_map.csv` or an equivalent for the specified tweet collection.

- **Output data:** 

  Contained in `./output/` by default. 

The required packages are specified at the top of  `part_1.ipynb`. Note specially,  ` nltk.stopwords` and `nltk.punkt` should be installed if not present.

### Functionality

The programs takes as input the `tw_hurricane_data.json` and `tweet_document_ids_map.csv`, reads both files and builds a data frame which is exported to `./output/` as `tweets_df.csv`.  The data frame consists only of the fundamental information of the tweet and the text data is pre-processed.

The script can be run directly.



## Part 2: Indexing and Evaluation

### Before running

Verify that the correct data in each of the input/output folders exists:

- **Input data:**
  - `evaluation_gt.csv`

- **Output data:** 

  Contained in `./output/` by default. Should contain:

  - `tweets_df.csv` (output from `part_1.ipynb`)
  - `judges_evaluation_gt.csv` (may be updated during execution)

The required packages are specified at the top of  `part_2.ipynb`. 

### Functionality

The programs takes as input the `tweets_df.csv` generated in the previous part. Builds an index for each term in the collection of tweets and stores term frequencies and inverse document frequencies. The program then takes a set of queries and evaluates the ranking performance based on the ground truth provided by `evaluation_gt.csv`. Similarly the user can build a ground truth for another set of queries that will be stored in `judges_evaluation_gt.csv`. A default version of this file is provided.

The script can be run directly.

## Part 3: Ranking

### Before running

Verify that the correct data in each of the input/output folders exists:

- **Output data:** 

  Contained in `./output/` by default. Should contain:

  - `tweets_df.csv` (output from `part_1.ipynb`)

The required packages are specified at the top of  `part_3.ipynb`. 

### Functionality

The programs takes as input the `tweets_df.csv` generated in part 1. Builds an index for each term in the collection of tweets and stores term frequencies and inverse document frequencies. The program then takes a set of queries and performs a ranking in 4 different ways: 
- TF-IDF + Cosine Similariy
- BM25
- Weighted TF-IDF plus tweet relevance (hashtags, likes, retweets) See report.
- Tweet2Vec (mean word2vec representation of the terms) + Cosine Similarity

The script can be run directly.

## Part 4: User interface and web analytics

### Before running

The folder for this part is individual.

Berify that the root directory contains:

  - `tw_hurricaine_data_indexed.json` (modified input for `part_1.ipynb`)

The required packages are specified at the top of each python script.

### Functionality

The application reads the JSON file an preprocesses all tweets (as in Part 1). This information is partially stored using MongoDB. Then application offers a search functionality and returns a ranking of documents based on the selected ranking function. The application also has other pages for exploring the results and visualising some web statistics.

To run the application execute `web_app.py` and visit http://127.0.0.1:8088.



