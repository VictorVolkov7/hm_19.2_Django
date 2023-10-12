from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    title = models.TextField(**NULLABLE, verbose_name='описание')
    preview = models.ImageField(upload_to='catalog/', **NULLABLE, verbose_name='изображение')
    category = models.ForeignKey('Category', verbose_name='категория', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='цена за покупку')
    creation_date = models.DateTimeField(verbose_name='дата создания')
    last_change_date = models.DateTimeField(verbose_name='дата последнего изменения')

    def __str__(self):
        return f'{self.category} {self.name}({self.title}) {self.price}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    title = models.TextField(**NULLABLE, verbose_name='описание')

    def __str__(self):
        return f'{self.name}({self.title})'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Contacts(models.Model):
    phone = models.CharField(max_length=20, verbose_name='телефон')
    telegram = models.CharField(max_length=50, verbose_name='телеграмм')
    vk = models.CharField(max_length=50, verbose_name='ВКонтакте')

    def __str__(self):
        return f'{self.phone} {self.telegram} {self.vk}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='заголовок')
    slug = models.CharField(max_length=50, verbose_name='slug', **NULLABLE)
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    date_create = models.DateField(verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='признак публикации')
    count_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    version_number = models.CharField(max_length=20, verbose_name='номер версии')
    version_name = models.CharField(max_length=50, verbose_name='название версии')
    is_active = models.BooleanField(verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.version_name}({self.version_number})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
