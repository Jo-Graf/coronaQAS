import hashlib
import re
from typing import Optional, List
import pandas as pd

from backend_app.qas_core.qas_data_loader import QASDataLoader
from backend_app.qas_core.qas_database import QASDatabase
from backend_app.qas_core.qas_document import QASDocument

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import CountVectorizer

from spacy.lang.en import English
from spacy.tokenizer import Tokenizer

import numpy as np


class QASLDA:

    DF_COLUMNS = ['id', 'title', 'full_text']

    def __init__(self,
                 database: Optional[QASDatabase] = None,
                 doc_query: Optional[str] = None,
                 docs_queries: Optional[str] = None,
                 num_topics: Optional[int] = 6,
                 doc_topic_prior: Optional[float] = 0.20473924934073703,
                 topic_word_prior: Optional[float] = 2.175756258808697,
                 num_words: Optional[int] = 20,
                 max_df: Optional[float] = 2,
                 min_df: Optional[float] = 0.95,
                 stop_words: Optional[str] = 'english'):
        self.database = database
        self.doc_query = doc_query
        self.docs_queries = docs_queries
        # self.doc_parts = []
        self.doc = None
        self.num_topics = num_topics
        self.num_words = num_words
        self.max_df = max_df
        self.min_df = min_df
        self.stop_words = stop_words
        self.docs = pd.DataFrame(columns=QASLDA.DF_COLUMNS)
        self.nlp = English()
        self.tokenizer = self.nlp.Defaults.create_tokenizer(self.nlp)
        self.doc_topic_prior = doc_topic_prior
        self.topic_word_prior = topic_word_prior

    def _docs_to_string(self, docs: List[QASDocument]) -> pd.DataFrame:
        title = docs[0].meta['title']
        full_text = title
        doc_id = None
        for doc in docs:
            if doc.meta['is_doc_meta'] is not True:
                full_text += '\n' + doc.meta['subtitle']
                full_text += '\n' + doc.text
            else:
                doc_id = doc.id

        return pd.DataFrame(columns=QASLDA.DF_COLUMNS, data=[[doc_id, title, full_text]])

    def load(self) -> List[List[str]]:
        # based on: https://towardsdatascience.com/setting-up-text-preprocessing-pipeline-using-scikit-learn-and-spacy-e09b9b76758f

        doc_parts = self.database.get_data(query=self.doc_query)
        self.doc = self._docs_to_string(doc_parts)

        for query in self.docs_queries:
            curr_doc_parts = self.database.get_data(query=query)
            self.docs = self.docs.append(self._docs_to_string(curr_doc_parts))

        all_docs = self.doc.append(self.docs)

        all_docs_text = all_docs.full_text.values

        spacy_estimators = [('tokenizer', self.pipelinize(self.spacy_tokenizer)),
                            ('preprocessor', self.pipelinize(self.punctation_removal)),
                            ('string_converter', self.pipelinize(self.string_converter))
                            ]

        spacy_pipe = Pipeline(spacy_estimators)

        preprocessed_train_docs = [spacy_pipe.transform([x])[0] for x in all_docs_text]
        # cv = CountVectorizer(max_df=self.max_df, min_df=self.min_df, stop_words=self.stop_words)
        cv = CountVectorizer(strip_accents='unicode', token_pattern=r'\b[a-zA-Z]{3,}\b')
        train_input = cv.fit_transform(preprocessed_train_docs[1:]) # omit target doc

        model = LatentDirichletAllocation(n_components=self.num_topics,
                                          doc_topic_prior=self.doc_topic_prior,
                                          topic_word_prior=self.topic_word_prior,
                                          random_state=42,
                                          learning_method='online')
        model.fit(train_input)

        topics = []
        words = cv.get_feature_names()
        topic_word_probabilities = model.components_ / model.components_.sum(axis=1)[:, np.newaxis]

        for index, topic in enumerate(model.components_):
            words_in_topic = [words[i] for i in topic.argsort()[-self.num_words:]]
            word_probabilities = [(topic_word_probabilities[index][i]/topic_word_probabilities[index].sum())
                                  for i in topic.argsort()[-self.num_words:]]
            words_in_topic.reverse()
            word_probabilities.reverse()

            topics.append({
                'words': words_in_topic,
                'probabilities': word_probabilities
            })

        doc_topic_probabilities_input = cv.transform(preprocessed_train_docs)
        doc_topic_probabilities = model.transform(doc_topic_probabilities_input)

        relevant_probabilities = doc_topic_probabilities[0]/doc_topic_probabilities[0].sum()

        # based on: https://scikit-learn.org/stable/modules/neighbors.html
        nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(doc_topic_probabilities)
        distances, indices = nbrs.kneighbors(doc_topic_probabilities)

        nearest_indices = indices[0][1:]
        nearest_docs = [all_docs.id.values[x] for x in nearest_indices]

        result = {
            'id': self.doc.id.values[0],
            'topics': topics,
            'topic_probabilities': list(relevant_probabilities),
            'nearest_neighbours': nearest_docs
        }

        return result


    def pipelinize(self, function, active=True):
        # from: https://towardsdatascience.com/setting-up-text-preprocessing-pipeline-using-scikit-learn-and-spacy-e09b9b76758f
        def list_comprehend_a_function(list_or_series, active=True):
            if active:
                return [function(i) for i in list_or_series]
            else:  # if it's not active, just pass it right back
                return list_or_series

        return FunctionTransformer(list_comprehend_a_function, validate=False, kw_args={'active': active})

    def punctation_removal(self, text):
        # based on: https://towardsdatascience.com/setting-up-text-preprocessing-pipeline-using-scikit-learn-and-spacy-e09b9b76758f
        if isinstance((text), (str)):
            # text = re.sub('<[^>]*>', '', text)
            text = re.sub('[\W]+', '', text.lower())
            return text
        if isinstance((text), (list)):
            return_list = []
            for i in range(len(text)):
                # temp_text = re.sub('<[^>]*>', '', text[i])
                temp_text = text[i]
                temp_text = re.sub('[\W]+', '', temp_text.lower())
                if temp_text is not '':
                    return_list.append(temp_text)
            return return_list
        else:
            pass

    def spacy_tokenizer(self, text):
        # from: https://towardsdatascience.com/setting-up-text-preprocessing-pipeline-using-scikit-learn-and-spacy-e09b9b76758f
        tokens = self.tokenizer(text)

        lemma_list = []
        for token in tokens:
            if token.is_stop is False:
                lemma_list.append(token.lemma_)

        return lemma_list

    def string_converter(self, list_or_str, delimiter=' '):
        if isinstance(list_or_str, str):
            return list_or_str
        elif isinstance(list_or_str, list):
            # print('List is flattend to one dimension')
            list_input = np.array(list_or_str).reshape(-1)
            return delimiter.join(list_input)
        else:
            raise AttributeError('list_or_str parameter has wrong type')
