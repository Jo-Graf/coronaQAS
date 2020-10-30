import hashlib
from typing import Optional, List

from sklearn.feature_extraction.text import CountVectorizer

from backend_app.qas_core.qas_data_loader import QASDataLoader
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_document import QASDocument
from sklearn.decomposition import LatentDirichletAllocation


# TODO: add to uml
class QASLDA:

    def __init__(self,
                 database: Optional[QASDatabase] = None,
                 query: Optional[str] = None,
                 num_topics: Optional[int] = 5,
                 num_words: Optional[int] = 20,
                 max_df: Optional[float] = 2,
                 min_df: Optional[float] = 0.95,
                 stop_words: Optional[str] = 'english'):
        self.database = database
        self.query = query
        self.doc_parts = []
        self.doc_string = None
        self.num_topics = num_topics
        self.num_words = num_words
        self.max_df = max_df
        self.min_df = min_df
        self.stop_words = stop_words

    def _docs_to_string(self, docs: List[QASDocument]) -> str:
        title = docs[0].meta['title']
        full_text = title

        for doc in docs:
            if doc.meta['is_doc_meta'] is not True:
                full_text += '\n' + doc.meta['subtitle']
                full_text += '\n' + doc.text

        return full_text

    def load(self) -> List[List[str]]:
        self.doc_parts = self.database.get_data(query=self.query)
        self.doc_string = self._docs_to_string(self.doc_parts)

        # TODO: check min_df, max_df
        # cv = CountVectorizer(max_df=self.max_df, min_df=self.min_df, stop_words=self.stop_words)
        cv = CountVectorizer(stop_words=self.stop_words)
        df = cv.fit_transform([self.doc_string])

        lda = LatentDirichletAllocation(n_components=self.num_topics, random_state=42)
        lda.fit(df)

        topics = {}
        words = cv.get_feature_names()

        for index, topic in enumerate(lda.components_):
            words_in_topic = [words[i] for i in topic.argsort()[-self.num_words:]]
            unique_key = ''.join(words_in_topic).encode('utf-8')
            unique_hashed_key = hashlib.md5(unique_key).hexdigest()
            topics[unique_hashed_key] = words_in_topic

        return list(topics.values())
