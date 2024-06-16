from dashboard.api.serializer import ChildSerializer, UserSerializer
from dashboard.dao import ChildDAO, ContentDAO, UserDAO
from django.db.models import Q
from rest_framework import serializers
from rest_framework.views import APIView

from backend.helpers.common_helper import check_mysql_connection
from backend.helpers.custom_permission import APIKeyPermission
from backend.helpers.custom_response import ErrorResponse, SuccessResponse

from .serializer import BlogSerializer, VlogSerializer


class ServiceCheckAPI(APIView):

    permission_classes = (APIKeyPermission,)

    def get(self, request, version=1, format=None):
        context = {"status": "OK", "detail": "Dashboard Service Health Check API"}

        if not check_mysql_connection():
            context["status"] = "NOT_OK"
            context["detail"] = "Unable to connect with database"
            return ErrorResponse(context, status=500)
        return SuccessResponse(context, status=200)

class UserContentAPIView(APIView):

    permission_classes = (APIKeyPermission,)

    def get(self, request, version=1):
        user_id = request.GET.get('uid') if request.GET.get('uid') else request.user.id

        children = ContentDAO.get_children_for_user(user_id)
        if not children.exists():
            return SuccessResponse({"detail": "No children found for the user."}, status=400)

        blogs = ContentDAO.get_blogs_for_children(children)
        vlogs = ContentDAO.get_vlogs_for_children(children)

        response_data = []
        for child in children:
            child_blogs = blogs.filter(
                Q(keywords__entity_type='age_group', keywords__entity_id=child.age_group) |
                Q(keywords__entity_type='gender', keywords__entity_id=child.gender) |
                Q(keywords__entity_type='experience_level', keywords__entity_id=child.user.parent_type)
            ).distinct()

            child_vlogs = vlogs.filter(
                Q(keywords__entity_type='age_group', keywords__entity_id=child.age_group) |
                Q(keywords__entity_type='gender', keywords__entity_id=child.gender) |
                Q(keywords__entity_type='experience_level', keywords__entity_id=child.user.parent_type)
            ).distinct()

            child_data = {
                "title": f"Recommended Content for {child.name}",
                "blogs": BlogSerializer(child_blogs, many=True).data,
                "vlogs": VlogSerializer(child_vlogs, many=True).data
            }
            response_data.append(child_data)

        return SuccessResponse({"result": True, "data": response_data}, status=200)

class UserCreateAPIView(APIView):

    permission_classes = (APIKeyPermission,)

    def post(self, request, version, *args, **kwargs):
        try:
            user = UserDAO.create_user(request.data)
            return SuccessResponse(UserSerializer(user).data, status=201)
        except serializers.ValidationError as e:
            return ErrorResponse(e.detail, status=400)

class UserUpdateAPIView(APIView):

    permission_classes = (APIKeyPermission,)

    def put(self, request, user_id, version, *args, **kwargs):
        try:
            user = UserDAO.update_user(user_id, request.data)
            return SuccessResponse(UserSerializer(user).data, status=200)
        except serializers.ValidationError as e:
            return ErrorResponse(e.detail, status=400)

class ChildrenCreateUpdateAPIView(APIView):
    
    permission_classes = (APIKeyPermission,)

    
    def post(self, request, user_id, version, *args, **kwargs):
        try:
            children = ChildDAO.create_children_for_user(user_id, request.data)
            return SuccessResponse(ChildSerializer(children, many=True).data, status=201)
        except serializers.ValidationError as e:
            return ErrorResponse(e.detail, status=400)

    def put(self, request, user_id, *args, **kwargs):
        try:
            children = ChildDAO.update_children_for_user(user_id, request.data)
            return SuccessResponse(ChildSerializer(children, many=True).data, status=200)
        except serializers.ValidationError as e:
            return ErrorResponse(e.detail, status=400)
