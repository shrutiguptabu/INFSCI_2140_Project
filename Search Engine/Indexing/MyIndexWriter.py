import Classes.Path as Path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import RegexTokenizer
import pandas as pd
import pathlib

# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    writer=[]

    def __init__(self):
        rootPath = pathlib.Path(__file__).parent.parent.__str__()
        self.inputFilePath = rootPath + Path.CleanedDataFile

        schema = Schema(doc_no=ID(stored=True),
                        doc_content=TEXT(analyzer=RegexTokenizer(), stored=True))
        indexing = index.create_in(rootPath + Path.IndexPath, schema)
        self.writer = indexing.writer()
        return

    # This method build index for each document.
    def index(self, docNo, content):
        self.writer.add_document(doc_no=docNo, doc_content=content)
        return
    
    # This method build index for entire corpus.
    def indexCorpus(self):
        count = 0
    
        # Initiate pre-processed collection file reader.
        corpus = pd.read_csv(self.inputFilePath, encoding="utf-8")
        
        # Build index of corpus by product.
        for row in corpus.iterrows():
            self.index(str(row[1]['product_uid']), row[1]['bag_of_words_cleaned'])
            count+=1
            if count%5000==0:
                print("Finished indexing ", count," products")
        
        # Finish
        print("Totally finished, indexed ", count, " products")
        self.close()
        return

    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        self.writer.commit()
        return
