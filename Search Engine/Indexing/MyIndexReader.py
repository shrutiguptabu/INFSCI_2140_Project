import whoosh.index as index
from whoosh.reading import IndexReader
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.analysis import RegexTokenizer
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
import Classes.Path as Path
import pathlib

# Efficiency and memory cost should be paid with extra attention.
class MyIndexReader:

    searcher=[]

    def __init__(self):
        rootPath = pathlib.Path(__file__).parent.parent.__str__()
        
        self.searcher = index.open_dir(rootPath + Path.IndexPath).searcher()

    # Return DF.
    def ProductFreq(self, token):
        results = self.searcher.search(Term("product_description", token))
        return len(results)

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        results = self.searcher.search(Term("product_description", token), limit=None)
        count = 0
        for result in results:
            words = self.searcher.stored_fields(result.docnum)["product_description"].split(" ")
            for word in words:
                if word==token:
                    count+=1
        return count

    # Return posting list in form of {productID:frequency}.
    def getPostingList(self, token):
        results = self.searcher.search(Term("product_description", token), limit=None)
        postList = {}
        for result in results:
            print(result)
            words = self.searcher.stored_fields(result.docnum)["product_description"].split(" ")
            print(words)
            count=0
            for word in words:
                if word==token:
                    count+=1
            postList[result['product_id']]=count
            print(count)
            if count == 0:
                break
        return postList

    # Return the length of the requested product.
    def getProductDescriptionLength(self, productId):
        words = self.searcher.stored_fields(productId)["product_description"].split(" ")
        return len(words)
    
    # Return the total number of products in the index
    def getProductCount(self):
        return self.searcher.doc_count()
    
