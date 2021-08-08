from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

client = FaunaClient(secret="your-secret-here")

indexes = client.query(q.paginate(q.indexes()))

print(indexes)