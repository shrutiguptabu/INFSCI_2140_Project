# import GenerateBagOfWords.BagOfWords as BagOfWords
import datetime

import DataCleaning.DataMerge as DataMerge
from BagOfWords import GenerateBagOfWords
import Indexing.MyIndexWriter as MyIndexWriter
import Indexing.MyIndexReader as MyIndexReader
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.ExtractQuery as ExtractQuery


def dataCleaning():
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
    
def indexBuild():
    indexWriter = MyIndexWriter.MyIndexWriter()
    indexWriter.indexCorpus()

def indexRead(term):
    index = MyIndexReader.MyIndexReader()
    # retrieve the token.
    df = index.ProductFreq(term)
    ctf = index.CollectionFreq(term)
    print(" >> the token \""+term+"\" appeared in "+ str(df) +" documents and "+ str(ctf) +" times in total")
    if df > 0:
        posting = index.getPostingList(term)
        for docId in posting:
            print("Product-Id: " + str(docId) + "\t Frequency: " + str(posting[docId]))

def qrmSearch():
    index = MyIndexReader.MyIndexReader()
    search = QueryRetreivalModel.QueryRetrievalModel(index)
    extractor = ExtractQuery.ExtractQuery()
    queries= extractor.getQuries()
    
    for query in queries:
        print(query.queryId,"\t",query.queryContent)
        results = search.retrieveQuery(query, 20)
        rank = 1
        for result in results:
            print(query.getQueryId()," Q0 ",result.getProductId(),' ',rank," ",result.getScore()," MYRUN",)
            rank +=1


startTime = datetime.datetime.now()
print('Start Time: ', startTime)

#dataCleaning()

#indexBuild()

indexRead('assembly')

#qrmSearch()


endTime = datetime.datetime.now()
print('End Time: ', endTime)
print('Total Time: ', endTime - startTime)
