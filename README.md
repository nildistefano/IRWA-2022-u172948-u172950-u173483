# IRWA-2022-u172948-u172950-u173483

### Authors

- Pol Ayala: u173483
- Toni Carbonell: u172950
- Nil Distefano: u172948

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
