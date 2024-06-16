from dashboard.models import Blog, Child, Keyword, User, Vlog
from rest_framework import serializers


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['entity_type', 'entity_id', 'keyword_name', 'created_on', 'updated_on']

class BlogSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True)
    created_by = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = ['title', 'content', 'keywords', 'created_on', 'updated_on', 'created_by', 'updated_by']

class VlogSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True)
    created_by = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = Vlog
        fields = ['title', 'video_url', 'keywords', 'created_on', 'updated_on', 'created_by', 'updated_by']

class ChildBlogsVlogsSerializer(serializers.Serializer):
    title = serializers.CharField()
    blogs = BlogSerializer(many=True)
    vlogs = VlogSerializer(many=True)

class UserSerializer(serializers.ModelSerializer):
    parent_type_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'parent_type', 'parent_type_display', 'first_name', 'last_name']

    def get_parent_type_display(self, obj):
        return dict(User.PARENT_TYPE_CHOICES).get(obj.parent_type)

class ChildSerializer(serializers.ModelSerializer):
    gender_display = serializers.SerializerMethodField()
    age_group_display = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = ['id', 'name', 'gender', 'gender_display', 'birth_date', 'age', 'age_group', 'age_group_display', 'created_on', 'updated_on']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
        }

    def get_gender_display(self, obj):
        return dict(Child.GENDER_CHOICES).get(obj.gender)

    def get_age_group_display(self, obj):
        return dict(Child.AGE_GROUPS).get(obj.age_group)