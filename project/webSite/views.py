from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from webSite.forms import  UserEditForm, ProfileEditForm

from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated


from .models import Order, Profile
from .permissions import IsAdminOrReadOnly, IsOwner, IsAdminAndDTUPStatus
from .serializers import OrderSerializer, OrderSerializer2
from rest_framework import generics




def home(request):
    return HttpResponse(request, "Main page")

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'webSite/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})



class OrderAPIList(generics.ListCreateAPIView):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' and not self.request.user.is_superuser:
            return OrderSerializer
        elif self.request.method == 'POST' and  self.request.user.is_superuser:
            return OrderSerializer2
        elif self.request.method == 'GET':
            return OrderSerializer2


    permission_classes = (IsAuthenticated,)


# class OrderAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     # permission_classes = (IsOwnerOrReadOnly, )
#     permission_classes = (IsAuthenticated, IsOwner, IsAdminAndDTUPStatus, )

class OrderAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_superuser or (self.request.method == 'GET' and self.request.user.is_authenticated):
            return OrderSerializer2
        elif self.request.user.is_authenticated and not self.request.user.is_superuser:
            return OrderSerializer

    permission_classes = (IsOwner, )



class OrderAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwner, )


def GetProfile(request, pk):
    me = Profile.objects.get(pk=pk)
    d = me.get_age()
    return HttpResponse(f'{d}')





