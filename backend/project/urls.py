from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

# #blog
# router.register('blog',BlogList,basename='blog')
# router.register('blog/<int:pk>',BlogDetail,basename='blog')
# #tag
# router.register('tag',TagViewSet,basename='tag')

urlpatterns=[
    path('blog/', BlogList.as_view()),
    path('blog/<int:pk>/', BlogDetail.as_view()),

    path('tag/', TagList.as_view()),
    path('tag/<int:pk>/', TagDetail.as_view()),
]


urlpatterns= format_suffix_patterns(urlpatterns)
