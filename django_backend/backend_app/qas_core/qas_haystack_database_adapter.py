from typing import List
from backend_app.qas_core.qas_database_variant import QASDatabaseVariant
from backend_app.qas_core.qas_document import QASDocument


class QASHaystackDatabaseAdapter(QASDatabaseVariant):

    def add_data(self, data: List[QASDocument]):
        pass

    def get_data(self) -> List[QASDocument]:
        pass
