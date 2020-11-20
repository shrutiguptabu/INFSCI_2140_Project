# import GenerateBagOfWords.BagOfWords as BagOfWords
import datetime

import DataCleaning.DataMerge as DataMerge
from BagOfWords import GenerateBagOfWords

startTime = datetime.datetime.now()
print('Start Time: ', startTime)

data_load_attributes = DataMerge.DataMerge()
data_load_attributes.data_load_attributes()

data_load_product_description = DataMerge.DataMerge()
data_load_product_description.data_load_product_description()

data_load_train = DataMerge.DataMerge()
data_load_train.data_load_train()

store_cleaned_data_with_relevance = DataMerge.DataMerge()
store_cleaned_data_with_relevance.store_cleaned_data_with_relevance()

store_cleaned_data_without_relevance = DataMerge.DataMerge()
store_cleaned_data_without_relevance.store_cleaned_data_without_relevance()

bag_of_words = GenerateBagOfWords.BagOfWords()
bag_of_words.bag_of_words()

endTime = datetime.datetime.now()
print('End Time: ', endTime)
print('Total Time: ', endTime - startTime)
