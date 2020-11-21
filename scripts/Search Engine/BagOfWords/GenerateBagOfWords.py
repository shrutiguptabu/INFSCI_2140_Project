import pathlib
import re

import pandas as pd
from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize

import Classes.Path as Path

stop = stopwords.words('english')
stop_words = set(stopwords.words('english'))


class BagOfWords:

    def __init__(self):
        return

    def bag_of_words(self):
        root = pathlib.Path(__file__).parent.parent.__str__()

        result_df = pd.read_csv(root + Path.DataWithoutRelevance)
        result_df["bag_of_words"] = result_df["name"] + result_df["value"] + result_df["product_description"]
        del result_df["name"]
        del result_df["value"]
        del result_df["product_description"]
        print('Bag of words generation')
        print(result_df.head(10))

        result_df["bag_of_words_cleaned"] = result_df["bag_of_words"].apply(
            lambda words: ' '.join(word.strip().lower() for word in words.split(",") if word not in stop))

        # remove the regular expression
        for index, row in result_df.iterrows():
            result_df.loc[index, 'bag_of_words_cleaned'] = (re.sub('[^a-zA-Z0-9 \n]', '', row['bag_of_words_cleaned']))

        # Instantiate the RegexpTokenizer
        tokenizer = RegexpTokenizer(r'\w+')

        # change the bag of words to string
        print("Tokenization in progress.")
        result_df['bag_of_words_cleaned'] = result_df['bag_of_words_cleaned'].astype("str")

        result_df['bag_of_words_cleaned'] = result_df['bag_of_words_cleaned'].replace("in", "")

        # tokenize the string
        result_df['bag_of_words_cleaned'] = result_df['bag_of_words_cleaned'].apply(lambda x: tokenizer.tokenize(x))

        def remove_stopwords(text):

            words = [w for w in text if w not in stop_words]
            return words

        print("Stopwords removal in progress.")
        result_df['bag_of_words_cleaned'] = result_df['bag_of_words_cleaned'].apply(lambda x: remove_stopwords(x))

        # instantiate lemmatizer
        lemmatizer = WordNetLemmatizer()

        def word_lemmatizer(text):
            lem_text = [lemmatizer.lemmatize(i) for i in text]
            return lem_text

        print("Lemmatization in progress.")
        result_df['bag_of_words_cleaned'] = result_df['bag_of_words_cleaned'].apply(lambda x: word_lemmatizer(x))

        # instantiate stemmer
        stemmer = PorterStemmer()

        def word_stemmer(text):
            stem_text = " ".join([stemmer.stem(i) for i in text])
            return stem_text

        print("Word Stemming in progress.")
        result_df['bag_of_words_cleaned'] = result_df['bag_of_words_cleaned'].apply(lambda x: word_stemmer(x))
        result_df['bag_of_words_cleaned'] = result_df['bag_of_words_cleaned'].astype(str)

        # count = collections.Counter(result_df['bag_of_words_cleaned'][:1])

        processed_text = []

        for i in result_df['bag_of_words_cleaned']:
            text = i.strip()
            processed_text.append(word_tokenize(str(text)))

        # total_vocab = [x for x in result_df]

        print("Final result_df")
        print(result_df.head(10))

        del result_df['bag_of_words']
        cleaned_df = result_df[['product_uid', 'search_term', 'product_title', 'bag_of_words_cleaned']]
        csv_path = root + Path.IntermediateOutputFiles + "Cleaned_Data.csv"
        cleaned_df.to_csv(csv_path)
