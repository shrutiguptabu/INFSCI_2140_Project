import Classes.Query as Query
import Classes.Product as Product
from collections import OrderedDict
from collections import defaultdict

class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        
        # Length of the entire corpus
        productCount = self.indexReader.getProductCount()
        self.corpusLength = self.calc_coll_len(productCount)
        
        # Set the parameter value
        self.muVal = 2000
        
        # Define Cache Dictionaries
        self.termCorpusFreq = defaultdict(int)
        self.termProductFreq = defaultdict(dict)
        self.productDescriptionLength = defaultdict(int)
        
        return


    # query:  The query to be searched for.
    # topN: The maximum number of returned products.
    # The returned results (retrieved products) should be ranked by the score (from the most relevant to the least).
    def retrieveQuery(self, query, topN):
        # Get matching products
        queryTokens = query.getQueryContent().split()
        
        # Store products in a dictionary
        products = defaultdict(int)
        
        # Extract Unique Products
        for term in queryTokens:
            postings = self.indexReader.getPostingList(term)
            self.setTermProductFreq(term, postings)
            for productId in postings.keys():
                products[productId] = ""
        
        for productId in products.keys():

            # Calculate score            
            score = self.dirichletSmoothing(queryTokens, productId)
            
            # Populate a new product
            newProduct = Product.Product()
            newProduct.setProductId(productId)
            newProduct.setScore(score)
            
            products[productId] = newProduct
        
        return [v for v in sorted(products.values(), key=lambda product: product.getScore(), reverse = True)][:topN]
    
    # Query likelihood language model
    def dirichletSmoothing(self, terms, productId):
        score = 1.0 # Default the score to 1
        productDescLen = self.getProductDescriptionLength(productId)
        adjustedLength = productDescLen + self.muVal
        
        l1 = productDescLen / adjustedLength
        r1 = self.muVal / adjustedLength
        
        for term in terms:
            termCorpusFreq = self.getTermCorpusFreq(term)
            if termCorpusFreq:
                productTermFrequency = self.getTermProductFreq(term, productId)
                l2 = productTermFrequency / productDescLen
                r2 = termCorpusFreq / self.corpusLength
                score = score * (l1 * l2 + r1 * r2)
        return score
    
    # Term Corpus Frequency
    def getTermCorpusFreq(self, term):
        if term in self.termCorpusFreq:
            termFreq = self.termCorpusFreq[term]
        else:
            termFreq = self.indexReader.CollectionFreq(term)
            self.termCorpusFreq[term] = termFreq
        return termFreq
    
    # Product Description Length
    def getProductDescriptionLength(self, productId):
        productDescLen = self.productDescriptionLength[productId]
        if not productDescLen:
            productDescLen = self.indexReader.getProductDescriptionLength(productId)
            self.productDescriptionLength[productId] = productDescLen
        return productDescLen
    
    # Term Product Description Frequency
    def getTermProductFreq(self, term, productId):
        try:
            termProductFreq = self.termProductFreq[term][productId] 
        except KeyError:
            termProductFreq = 0
        return termProductFreq
    
    # Set Term Product frequency
    def setTermProductFreq(self, term, postings):
        termData = self.termProductFreq[term]
        if not termData:
            self.termProductFreq[term] = postings
          
    # Calculate number of terms in the corpus
    def calc_coll_len(self, productCount):
        coll_len = 0
        for i in range(productCount):
            coll_len = coll_len + self.indexReader.getProductDescriptionLength(i)
        return coll_len