from elasticsearch_dsl import analyzer, tokenizer

__all__ = (
    'html_strip', 'search_analyzer', 'substance_name_analyzer', 'substance_number_analyzer', 'limit_scope_analyzer',
    'region_analyzer', 'task_name_analyzer', 'user_name_analyzer', 'case_insensitive_sort_analyzer'
)

_filters = ['lowercase', 'stop', 'snowball']

html_strip = analyzer(
    'html_strip',
    tokenizer='lowercase',
    filter=_filters,
    char_filter=['html_strip']
)

'''
edge_ngram tokenizer
docs: https://www.elastic.co/guide/en/elasticsearch/reference/1.6/analysis-edgengram-tokenizer.html
'''
search_analyzer = analyzer(
    'search_analyzer',
    tokenizer=tokenizer('trigram', 'edge_ngram', min_gram=3, max_gram=5, token_chars=['letter', 'digit']),
    filter=_filters
)

'''
edge_ngram tokenizer
docs: https://www.elastic.co/guide/en/elasticsearch/reference/1.6/analysis-edgengram-tokenizer.html
'''
substance_name_analyzer = analyzer(
    'substance_name_analyzer',
    tokenizer=tokenizer('substance_trigram', 'ngram', min_gram=3, max_gram=3, token_chars=['letter', 'digit']),
    filter=_filters
)

substance_number_analyzer = analyzer(
    'substance_number_analyzer',
    tokenizer='standard',
    filter=['lowercase', 'stop', 'snowball', 'word_delimiter_graph']
)
'''
ngram tokenizer
docs: https://www.elastic.co/guide/en/elasticsearch/reference/1.6/analysis-ngram-tokenizer.html
'''
# search_analyzer = analyzer(
#     'search_analyzer',
#     tokenizer=tokenizer('trigram', 'ngram', min_gram=4, max_gram=5),
#     filter=_filters
# )

limit_scope_analyzer = analyzer(
    'limit_scope_analyzer',
    tokenizer=tokenizer('scope_trigram', 'ngram', min_gram=3, max_gram=3, token_chars=['letter', 'digit']),
    filter=_filters
)

region_analyzer = analyzer(
    'region_analyzer',
    tokenizer=tokenizer('region_trigram', 'edge_ngram', min_gram=2, max_gram=3, token_chars=['letter', 'digit']),
    filter=_filters
)


task_name_analyzer = analyzer(
    'task_name_analyzer',
    tokenizer=tokenizer('task_name_analyzer', 'edge_ngram', min_gram=3, max_gram=3, token_chars=['letter', 'digit']),
    filter=_filters
)

user_name_analyzer = analyzer(
    'user_name_analyzer',
    tokenizer=tokenizer('user_name_analyzer', 'edge_ngram', min_gram=3, max_gram=5, token_chars=['letter', 'digit']),
    filter=_filters
)

case_insensitive_sort_analyzer = analyzer(
    'case_insensitive_sort_analyzer',
    tokenizer='keyword',
    filter=_filters
)
