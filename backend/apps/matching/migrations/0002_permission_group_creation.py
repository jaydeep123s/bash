# Generated by Django 3.0.7 on 2020-06-15 12:28

from django.db import migrations


# This is added here and not in the project because these names are know to be valid only
# in at this very moment in time - later migrations could alter them.
# Thus we only need them here for now. Saving these as constants elsewhere for easy usability
# in the project is a different thing, but probably unnecessary when we can use decorators.
class NewPermissions:
    can_approve_type_a = "can_approve_type_a"
    can_approve_type_b = "can_approve_type_b"
    can_view_user_stats = "can_view_user_stats"
    can_view_access_stats = "can_view_access_stats"


class Migration(migrations.Migration):
    def create_permissions(apps, schema_editor):
        # We can't import the models directly as they may be a newer
        # version than this migration expects. We use the historical version.
        Permission = apps.get_model("auth", "Permission")
        ContentType = apps.get_model("contenttypes", "ContentType")
        Staff = apps.get_model("matching", "Staff")
        ParticipantA = apps.get_model("matching", "ParticipantA")
        ParticipantB = apps.get_model("matching", "ParticipantB")

        # We have to choose contenttypes for our permissions. For more ideas, refer to
        # https://stackoverflow.com/a/13933002
        content_type_staff = ContentType.objects.get_for_model(Staff)
        content_type_participanta = ContentType.objects.get_for_model(ParticipantA)
        content_type_participantb = ContentType.objects.get_for_model(ParticipantB)

        permission_list = [
            {
                "codename": NewPermissions.can_approve_type_a,
                "name": "Can approve type A users",
                "content_type": content_type_participanta,
            },
            {
                "codename": NewPermissions.can_approve_type_b,
                "name": "Can approve type B users",
                "content_type": content_type_participantb,
            },
            {
                "codename": NewPermissions.can_view_user_stats,
                "name": "Can view user statistics",
                "content_type": content_type_staff,
            },
            {
                "codename": NewPermissions.can_view_access_stats,
                "name": "Can view access statistics",
                "content_type": content_type_staff,
            },
        ]

        for permission in permission_list:
            Permission.objects.create(**permission)

    def delete_permissions(apps, schema_editor):
        Permission = apps.get_model("auth", "Permission")

        permission_list = [
            NewPermissions.can_approve_type_a,
            NewPermissions.can_approve_type_b,
            NewPermissions.can_view_user_stats,
            NewPermissions.can_view_access_stats,
        ]

        Permission.objects.filter(codename__in=permission_list).delete()

    def create_groups(apps, schema_editor):
        Group = apps.get_model("auth", "Group")
        Permission = apps.get_model("auth", "Permission")

        group_is_a, created = Group.objects.get_or_create(name="is_a")
        group_is_b, created = Group.objects.get_or_create(name="is_b")
        group_is_a_approved, created = Group.objects.get_or_create(name="approved_a")
        group_is_b_approved, created = Group.objects.get_or_create(name="approved_b")
        group_perm_user_stats, created = Group.objects.get_or_create(name="perm_user_stats")
        group_perm_access_stats, created = Group.objects.get_or_create(name="perm_access_stats")
        group_perm_approve_a, created = Group.objects.get_or_create(name="perm_approve_a")
        group_perm_approve_b, created = Group.objects.get_or_create(name="perm_approve_b")

        can_approve_type_a = Permission.objects.get(codename=NewPermissions.can_approve_type_a)
        group_perm_approve_a.permissions.add(can_approve_type_a)

        can_approve_type_b = Permission.objects.get(codename=NewPermissions.can_approve_type_b)
        group_perm_approve_b.permissions.add(can_approve_type_b)

        can_view_user_stats = Permission.objects.get(codename=NewPermissions.can_view_user_stats)
        group_perm_user_stats.permissions.add(can_view_user_stats)

        can_view_access_stats = Permission.objects.get(
            codename=NewPermissions.can_view_access_stats
        )
        group_perm_access_stats.permissions.add(can_view_access_stats)

    def delete_groups(apps, schema_editor):
        Group = apps.get_model("auth", "Group")

        group_list = [
            "is_a",
            "is_b",
            "approved_a",
            "approved_b",
            "perm_user_stats",
            "perm_access_stats",
            "perm_approve_a",
            "perm_approve_b",
        ]

        Group.objects.filter(name__in=group_list).delete()

    def update_existing_users_with_group(apps, schema_editor):
        User = apps.get_model("matching", "User")
        Group = apps.get_model("auth", "Group")
        group_is_a = Group.objects.get(name="is_a")
        group_is_b = Group.objects.get(name="is_b")
        group_perm_user_stats = Group.objects.get(name="perm_user_stats")
        group_perm_access_stats = Group.objects.get(name="perm_access_stats")
        group_perm_approve_a = Group.objects.get(name="perm_approve_a")
        group_perm_approve_b = Group.objects.get(name="perm_approve_b")

        users_a = User.objects.filter(is_A=True)
        users_b = User.objects.filter(is_B=True)
        users_staff = User.objects.filter(is_staff=True)

        # Quick reminder on python syntax: the star operator unpacks
        # sequences into positional arguments
        group_is_a.user_set.add(*users_a)
        group_is_b.user_set.add(*users_b)
        group_perm_user_stats.user_set.add(*users_staff)
        group_perm_access_stats.user_set.add(*users_staff)
        group_perm_approve_a.user_set.add(*users_staff)
        group_perm_approve_b.user_set.add(*users_staff)

    def remove_groups_from_users(apps, schema_editor):
        # Not really necessary since on reverse the groups will get deleted either way
        pass

    dependencies = [
        ("matching", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_permissions, reverse_code=delete_permissions),
        migrations.RunPython(create_groups, reverse_code=delete_groups),
        migrations.RunPython(
            update_existing_users_with_group, reverse_code=remove_groups_from_users
        ),
    ]
