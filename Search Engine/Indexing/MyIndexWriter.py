from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import RegexTokenizer
import Classes.Path as Path
import pandas as pd
import pathlib

# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    writer=[]

    def __init__(self):
        rootPath = pathlib.Path(__file__).parent.parent.__str__()
        self.inputFilePath = rootPath + Path.DataWithoutRelevance

        schema = Schema(docId=ID(stored=True),
                        doc_content=TEXT(analyzer=RegexTokenizer(), stored=True))
        indexing = index.create_in(rootPath + Path.IndexPath, schema)
        self.writer = indexing.writer()
        return
    
    def indexCorpus(self):
        count = 0
    
        # Initiate pre-processed collection file reader.
        corpus = pd.read_csv(self.inputFilePath, encoding="utf-8")
        
        # Build index of corpus document by document.
        for row in corpus.iterrows():
            self.index(str(row[1]['product_uid']), row[1]['product_description'])
            count+=1
            if count%5000==0:
                print("finish ", count," docs")
        
        # Finish
        print("totally finish ", count, " docs")
        self.close()
        return

    # This method build index for each document.
    def index(self, docId, content):
        self.writer.add_document(docId=docId, doc_content=content)
        return

    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        self.writer.commit()
        return
