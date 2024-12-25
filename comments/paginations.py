from rest_framework.pagination import PageNumberPagination

class CommentPagination(PageNumberPagination):
    page_query_param = 'comments_page'
    page_size = 8