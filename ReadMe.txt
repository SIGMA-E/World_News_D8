# Все операции выполнялись на операционной системе Linux Ubuntu (python 3.10.6)
-------------------------------------------------------------------------
# переходим в папку News проекта WorldNews(где расположен файл manage.py):
cd WorldNews/News/

# активируем консоль Python:
python3 manage.py shell

# импортируем все из модели "models.py" приложения "news_portal":
from news_portal.models import *
----------------------------------------------------------------------------------------------------

1. Создаем двух пользователей с помощью метода:
User.objects.create_user('Alex')
User.objects.create_user('Maxim')

# проверим созданных пользователей:
User.objects.all().values('id', 'username')
----------------------------------------------------------------------------------------------------

2. Создаем два объекта модели "Author", связанные с пользователями:

# создадим объекты "user_alex" и user_max связанные с пользователеми "Alex" и 'Maxim' соответственно
user_alex = User.objects.get(id=1)
user_max = User.objects.get(id=2)

# внесем созданные объекты в таблицу модели "Author"(связь поля "user" один-к-одному с моделью "User")
Author.objects.create(user=user_alex)
Author.objects.create(user=user_max)

# проверим созданных авторов:
Author.objects.all().values('id', 'user__username')
----------------------------------------------------------------------------------------------------

3. Добавим 4 категории в модель "Category":
Category.objects.create(name_category = 'Музыка')
Category.objects.create(name_category = 'Кино')
Category.objects.create(name_category = 'Наука')
Category.objects.create(name_category = 'Спорт')

# проверим внесенные категории в таблицу модели "Category":
Category.objects.all().values()
----------------------------------------------------------------------------------------------------

4. Добавим 2 статьи и 1 новость в таблицу модели "Post":

# создадим авторов статей для поля "author" модели "Post":
author_alex = Author.objects.get(id=1)
author_max = Author.objects.get(id=2)

# внесем посты в таблицу модели "Post" под создаммыми авторами:
Post.objects.create(type_post='ar', title='Заголовок поста №1', text_post='Содержание поста №1', aurhor=author_alex)
Post.objects.create(type_post='ar', title='Заголовок поста №2', text_post='Содержание поста №2', aurhor=author_max)
Post.objects.create(type_post='nw', title='Заголовок поста №3', text_post='Содержание поста №3', aurhor=author_max)

# проверим внесенные посты по "id", "title":
Post.objects.all().values('id', 'title')
-----------------------------------------------------------------------------------------------------

5. Присвоим им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий)

# возьмем каждый пост как объект из модели "Post":
post_1 = Post.objrcts.get(id=1)
post_2 = Post.objects.get(id=2)
post_3 = Post.objects.get(id=3)

# возьмем каждую категорию как объект из модели "Category":
music = Category.objects.get(id=1)
muvie = Category.objects.get(id=2)
science = Category.objects.get(id=3)
sport = Category.objects.get(id=4)

# внесем объекты в таблицу модели "PostCategory" по 2 категории на один пост:
PostCategory.objects.create(post = post_1, category = science)
PostCategory.objects.create(post = post_1, category = sport)
PostCategory.objects.create(post = post_2, category = music)
PostCategory.objects.create(post = post_2, category = muvie)
PostCategory.objects.create(post = post_3, category = sport)
PostCategory.objects.create(post = post_2, category = muvie)

# проверим результат:
Post.objects.all().values('post', 'category')
-----------------------------------------------------------------------------------------------------

6. Создадим как минимум 4 комментария к разным объектам модели "Post" (в каждом объекте должен быть как минимум один комментарий).

# посты как объекты созданы в п 5 (post_1, post_2, post_3)
# объекты модели "User" создыны выше п. 2 (user_alex, user_max)
Comment.objects.create(text_comment='Комментарий к посту №1', post=post_1, user=user_max)
Comment.objects.create(text_comment='Комментарий к посту №2', post=post_2, user=user_alex)
Comment.objects.create(text_comment='Комментарий к посту №2', post=post_2, user=user_max)
Comment.objects.create(text_comment='Комментарий к посту №3', post=post_1, user=user_alex)

# проверим результат:
Comment.objects.all().values('id', 'user', 'text_comment')
-----------------------------------------------------------------------------------------------------

7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректируем рейтинги этих объектов.

# посты как объекты созданы в п 5 (post_1, post_2, post_3)
# увеличим рейтинг соответствующего поста каждый раз при вызове на +1
post_1.like()
post_2.like()
post_3.like()

# уменьшим рейтинг соответствующего поста каждый раз при вызове на -1
post_1.dislike()
post_2.dislike()
post_3.dislike()

# для корректировки рейтингов комментариев создадим объекты модели "Comment" зная "id" из п. 6:
comment_1 = Comment.object.get(id=1)
comment_2 = Comment.object.get(id=2)
comment_3 = Comment.object.get(id=3)
comment_4 = Comment.object.get(id=4)

# увеличим рейтинг соответствующего комментария каждый раз при вызове на +1
comment_1.like()
comment_2.like()
comment_3.like()
comment_4.like()

# уменьшим рейтинг соответствующего комментария каждый раз при вызове на -1
comment_1.dislike()
comment_1.dislike()
comment_1.dislike()
comment_1.dislike()
-----------------------------------------------------------------------------------------------------

8. Обновим рейтинги пользователей в модели "Author":

# авторы постов как объеты созданы в п.4 (author_alex, author_max)
author_alex.update_rating()
author_max.update_rating()
-----------------------------------------------------------------------------------------------------

9. Выведем username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта):
Author.objects.all().values('user__username', 'rating_autor').order_by('-rating_autor')[0]
-----------------------------------------------------------------------------------------------------

10. Выведем дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье:

# выведем лучшую статью по рейтингу:
Post.objects.all().values('time_post__date', 'author__user__username', 'rating_post', 'title').order_by('-rating_post').first()

# выведем превью лучшей статьи:
best_post = Post.objects.order_by('-rating_post')[0]
best_post.preview()
-----------------------------------------------------------------------------------------------------

11. Выведем все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

# отфильтруем все комментарии по "id" лучшего поста полученного через объект "best_post" созданного в п.10
Comment.objects.filter(post = best_post.id).values('time_comment__date','user__username', 'rating_comment', 'text_comment')
-----------------------------------------------------------------------------------------------------





























