from rest_framework.pagination import PageNumberPagination

class SnippetPagination(PageNumberPagination):
    page_query_param = 'snippets_page'
    page_size = 8