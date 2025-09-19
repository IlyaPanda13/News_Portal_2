from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from news.models import Post


class Command(BaseCommand):
    help = 'Управление группами и пользователями: создание групп, назначение прав, добавление пользователей в группы'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

        # Команда для создания групп
        create_parser = subparsers.add_parser('create_groups', help='Создает группы common и authors с правами')

        # Команда для добавления пользователя в группу
        add_user_parser = subparsers.add_parser('add_user', help='Добавляет пользователя в группу')
        add_user_parser.add_argument('username', type=str, help='Username пользователя')
        add_user_parser.add_argument('group', type=str, help='Название группы (common или authors)')

        # Команда для просмотра информации о группах
        info_parser = subparsers.add_parser('info', help='Показывает информацию о группах и их правах')

    def handle(self, *args, **options):
        command = options.get('command')

        if command == 'create_groups':
            self.create_groups()
        elif command == 'add_user':
            self.add_user_to_group(options['username'], options['group'])
        elif command == 'info':
            self.show_groups_info()
        else:
            self.stdout.write(
                self.style.ERROR('Неизвестная команда. Используйте: create_groups, add_user или info')
            )

    def create_groups(self):
        """Создает группы common и authors с соответствующими правами"""
        # Создаем группы
        common_group, created = Group.objects.get_or_create(name=settings.COMMON_GROUP_NAME)
        authors_group, created = Group.objects.get_or_create(name=settings.AUTHOR_GROUP_NAME)

        # Получаем ContentType для модели Post
        content_type = ContentType.objects.get_for_model(Post)

        # Назначаем права для common группы
        common_perms = Permission.objects.filter(
            content_type=content_type,
            codename__in=['view_post']
        )
        common_group.permissions.set(common_perms)

        # Назначаем права для authors группы
        author_perms = Permission.objects.filter(
            content_type=content_type,
            codename__in=['view_post', 'add_post', 'change_post', 'delete_post']
        )
        authors_group.permissions.set(author_perms)

        self.stdout.write(
            self.style.SUCCESS('Группы common и authors созданы с соответствующими правами')
        )

    def add_user_to_group(self, username, group_name):
        """Добавляет пользователя в группу"""
        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            self.stdout.write(
                self.style.SUCCESS(f'Пользователь {username} добавлен в группу {group_name}')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Пользователь {username} не найден')
            )
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Группа {group_name} не найдена')
            )

    def show_groups_info(self):
        """Показывает информацию о группах и их правах"""
        groups = Group.objects.all()

        if not groups.exists():
            self.stdout.write(self.style.WARNING('Группы не найдены'))
            return

        for group in groups:
            self.stdout.write(self.style.SUCCESS(f'\nГруппа: {group.name}'))
            self.stdout.write(f'Пользователи: {", ".join([user.username for user in group.user_set.all()])}')
            self.stdout.write('Права:')
            for perm in group.permissions.all():
                self.stdout.write(f'  - {perm.name}')