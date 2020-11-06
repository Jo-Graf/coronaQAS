from typing import Optional

from backend_app.qas_core.qas_document import QASDocument


# TODO: add to uml
class QASDocKeyGen:

    doc_separator = '-$-$-'

    @staticmethod
    def generate_key(base_key: str, count: int) -> str:
        return base_key + QASDocKeyGen.doc_separator + str(count)

    @staticmethod
    def get_doc_base_key(doc: Optional[QASDocument] = None, key: Optional[str] = None) -> str:
        if key is not None and doc is not None:
            raise AttributeError('Either key or doc has to None')

        id_array = None

        if doc is not None:
            id_array = doc.id.split(QASDocKeyGen.doc_separator)
        elif key is not None:
            id_array = key.split(QASDocKeyGen.doc_separator)

        return id_array[0]