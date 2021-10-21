from rest_framework import serializers
from .models import User


def update_user_account(full_name, phone_num, role, date_of_birth, bio, profile_pic_path, slug, username=null):
    user = User.objects.filter(phone_num=phone_num).update(
        full_name=full_name,
        role=role,
        date_of_birth=date_of_birth,
        bio=bio,
        profile_pic_path=profile_pic_path,
        slug=slug
    )

    return user
