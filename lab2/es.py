from os import listdir
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://elastic:elastic@localhost:9200/'],verify_certs=True)
index_name = 'test-index01'

#es.indices.delete(index_name)
es.indices.create(
    index=index_name,
    body={
      "settings": {
        "analysis": {
          "analyzer": {
            "polish": {
              "type": "custom",
                  "tokenizer": "standard",
                  "filter": [
                    "lowercase",
                    "synonym",
                    "morfologik_stem"
                  ]
                }
              },
              "filter": {
                "synonym": {
                  "type": "synonym",
                  "tokenizer": "standard",
                    "synonyms": [
                      "kpk, kodeks postępowania karnego",
                      "kpc, kodeks postępowania cywilnego",
                      "kk, kodeks karny",
                      "kc, kodeks cywilny"
                      ]
                    }
                  }
              }
      },
      "mappings": {
        "dynamic": "strict",
        "properties": {
          "text": {
            "type": "text",
            "analyzer": "polish",
            },
          "filename": {"type": "text"}
          }
        }
      }
    )

#zad 4,5
data = [f for f in listdir('dane')]
for i,file_name in enumerate(data):
    file = None
    with open('dane/'+file_name, 'r', encoding='utf-8') as f:
        file = f.read()
        dict_body = dict()
        dict_body["text"] = file
        dict_body['filename'] = file_name
        es.index(index=index_name, id=i, body=dict_body)
        if i%50==0:
            res = es.get(index=index_name, id=i)
            print(res)

#zad6
res= es.search(index=index_name,body={
  "query": {
    "match": {
      "text": {
        "query": "ustawa",
      }
    }
  }})
print('found {} documents containing \'usatawa\' in any form'.format(res['hits']['total']['value']))

#zad7
res= es.search(index=index_name,body={
  "query": {
    "match_phrase": {
      "text": {
        "query": "kodeks postępowania cywilnego",
        "slop": 0
      }
    }
  }
})
print('found {} documents containing \'kodeks postępowania cywilnego\' in any form'.format(res['hits']['total']['value']))

#zad8
res= es.search(index=index_name,body={
  "query": {
    "match_phrase": {
      "text": {
        "query":"wchodzi w życie",
        "slop": 2
      }
    }
  }
})
print('found {} documents containing \'wchodzi w życie\' in any form allowing up to 2 additional words'.format(res['hits']['total']['value']))

#zad9
res = es.search(index=index_name,body={
  "query": {
    "match": {
      "text": {
        "query": "ustawa"
       }
    }
  },
  "size": 10,
  "_source": [ "filename" ]
})

document_founds = len(res['hits']['hits'])
print('found top {} documents max score: {} min score: {}'.format(document_founds, res['hits']['hits'][0]['_score'], res['hits']['hits'][document_founds-1]['_score']))

#zad10
res= es.search(index=index_name,body={
  "query": {
    "match": {
      "text": {
        "query": "ustawa"
       }
    }
  },
  "size": 10,
  "_source": [ "filename" ],
  "highlight": {
    "number_of_fragments": 3,
    "fragment_size": 75,
    "fields": {
      "text": {}
    }
  }
})
for i,match in enumerate(res['hits']['hits']):
    print(str(i)+') '+ match['_source']['filename'] )
    for highlited_text in match['highlight']['text']:
        print('  '+  highlited_text)