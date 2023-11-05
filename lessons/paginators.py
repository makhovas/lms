from rest_framework.pagination import PageNumberPagination


class LessonPaginator(PageNumberPagination):
    page_size = 10


class CoursePaginator(PageNumberPagination):
    page_size = 5
