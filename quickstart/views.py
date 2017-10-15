from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from shop.models import Product , Table
from rest_framework import generics
from notifications.models import Notification
from quickstart.serializers import UserSerializer, GroupSerializer , ProductSerializer , TableSerializer , NotifSerializer , AllNotifSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class TableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class NotifViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Notification.objects.all()
    serializer_class = NotifSerializer

class AllNotif(generics.ListAPIView):
    serializer_class = AllNotifSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return Notification.objects.filter(to_user=username)
