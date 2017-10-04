__author__ = 'Marcel Verst'
__project__ = 'GeoEvaluator'
__className__ = 'Evaluator.py'
__version__ = '04.10.2017'

from Evaluator import Evaluator

temp = Evaluator()
query = "FROM xyz SELECT this"
temp.getData(query)