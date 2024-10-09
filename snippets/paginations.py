from rest_framework.pagination import PageNumberPagination

class SnippetPagination(PageNumberPagination):
    page_query_param = 'snippet_page'
    page_size = 6