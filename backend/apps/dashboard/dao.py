from datetime import datetime

from dashboard.api.serializer import ChildSerializer, UserSerializer
from django.db import transaction
from django.db.models import Q
from rest_framework import serializers

from .models import Blog, Child, Keyword, User, Vlog


class ContentDAO:
    @staticmethod
    def get_children_for_user(user_id):
        return Child.objects.filter(user_id=user_id).select_related('user')

    @staticmethod
    def get_keywords_for_user(user_id):
        children = ContentDAO.get_children_for_user(user_id)
        user = User.objects.get(id=user_id)
        experience_level = user.parent_type
        age_groups = children.values_list('age_group', flat=True)
        genders = children.values_list('gender', flat=True)

        return Keyword.objects.filter(
            Q(entity_type='age_group', entity_id__in=age_groups) |
            Q(entity_type='gender', entity_id__in=genders) |
            Q(entity_type='experience_level', entity_id=experience_level)
        ).distinct()

    @staticmethod
    def get_blogs_vlogs_for_user(user_id):
        keywords = ContentDAO.get_keywords_for_user(user_id)

        blogs = Blog.objects.filter(keywords__in=keywords).distinct().prefetch_related('keywords')
        vlogs = Vlog.objects.filter(keywords__in=keywords).distinct().prefetch_related('keywords')

        return blogs, vlogs

    @staticmethod
    def get_blogs_for_children(children):
        age_groups = children.values_list('age_group', flat=True)
        genders = children.values_list('gender', flat=True)
        user_ids = children.values_list('user_id', flat=True)
        experience_levels = User.objects.filter(id__in=user_ids).values_list('parent_type', flat=True)

        keywords = Keyword.objects.filter(
            Q(entity_type='age_group', entity_id__in=age_groups) |
            Q(entity_type='gender', entity_id__in=genders) |
            Q(entity_type='experience_level', entity_id__in=experience_levels)
        ).distinct()

        return Blog.objects.filter(keywords__in=keywords).distinct().prefetch_related('keywords')

    @staticmethod
    def get_vlogs_for_children(children):
        age_groups = children.values_list('age_group', flat=True)
        genders = children.values_list('gender', flat=True)
        user_ids = children.values_list('user_id', flat=True)
        experience_levels = User.objects.filter(id__in=user_ids).values_list('parent_type', flat=True)

        keywords = Keyword.objects.filter(
            Q(entity_type='age_group', entity_id__in=age_groups) |
            Q(entity_type='gender', entity_id__in=genders) |
            Q(entity_type='experience_level', entity_id__in=experience_levels)
        ).distinct()

        return Vlog.objects.filter(keywords__in=keywords).distinct().prefetch_related('keywords')


class UserDAO:
    @staticmethod
    @transaction.atomic
    def create_user(data):
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            password = data.get('password')
            if password:
                user.set_password(password)
                user.save()
            return user

    @staticmethod
    @transaction.atomic
    def update_user(user_id, data):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        user_serializer = UserSerializer(user, data=data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            password = data.get('password')
            if password:
                user.set_password(password)
                user.save()
            return user

class ChildDAO:

    @staticmethod
    @transaction.atomic
    def create_children_for_user(user_id, children_data):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        children = []
        for child_data in children_data:
            child_serializer = ChildSerializer(data=child_data)
            if child_serializer.is_valid(raise_exception=True):
                child = child_serializer.save(user=user)
                children.append(child)
        return children

    @staticmethod
    @transaction.atomic
    def update_children_for_user(user_id, children_data):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        keep_children = []
        for child_data in children_data:
            if 'birth_date' in child_data and isinstance(child_data['birth_date'], str):
                child_data['birth_date'] = datetime.strptime(child_data['birth_date'], '%Y-%m-%d').date()
            if "id" in child_data.keys():
                if Child.objects.filter(id=child_data["id"]).exists():
                    c = Child.objects.get(id=child_data["id"])
                    c.name = child_data.get('name', c.name)
                    c.gender = child_data.get('gender', c.gender)
                    c.birth_date = child_data.get('birth_date', c.birth_date)
                    c.save()
                    keep_children.append(c.id)
                else:
                    continue
            else:
                c = Child.objects.create(user=user, **child_data)
                keep_children.append(c.id)

        for child in user.children.all():
            if child.id not in keep_children:
                child.delete()

        return user.children.all()