from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from assimilation.models import Game

class UserAuthorization(Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(username=request.user.username)
        return object_list.none()

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = BasicAuthentication()
        authorization = UserAuthorization()



class GameAuthorization(Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(gameuser__user__username=request.user.username)
        return object_list.none()

class GameResource(ModelResource):
    # user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Game.objects.all().order_by('-created')
        resource_name = 'game'
        authentication = BasicAuthentication()
        authorization = GameAuthorization()