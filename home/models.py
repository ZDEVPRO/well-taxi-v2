from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.contrib.auth.hashers import make_password


class User(AbstractUser):
    type_users = (
        (1, "Admin"),
        (2, "Driver"),
        (3, "Customer"),
    )
    phone = models.CharField(max_length=25, null=True, blank=True)
    type = models.IntegerField(default=0, choices=type_users)
    firebase_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Price(models.Model):
    narx = models.CharField(max_length=600, default='Kelishiladi')

    def __str__(self):
        return self.narx

    class Meta:
        verbose_name = 'Narx'
        verbose_name_plural = 'Narxlar'


class Region(models.Model):
    nomi = models.CharField(max_length=600)

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = 'Viloyatlar'
        verbose_name_plural = 'Viloyatlar'


class Order(models.Model):
    STATUS = (
        ('yangi', 'Yangi'),
        ('kutish', 'Kutish'),
        ('olindi', 'Olindi')
    )

    PERSON_COUNT = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    )

    CLIENT_IN_CAR = (
        ('ha', 'Ha'),
        ('yoq', 'Yo`q')
    )

    status = models.CharField(max_length=100, choices=STATUS, default='yangi')
    qayerdan = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='qayerdanviloyat')
    qayerga = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='qayergadanviloyat')

    location = models.TextField(default='Manzil yo`q!')

    person_count = models.CharField(max_length=100, choices=PERSON_COUNT, default=1)
    price = models.ForeignKey(Price, on_delete=models.CASCADE, default='Kelishiladi', related_name='buyurtmanarxi')

    client_phone = models.CharField(max_length=100)
    client_name = models.CharField(max_length=200)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_customer')

    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver', blank=True, null=True)
    client_in_car = models.CharField(default='yoq', choices=CLIENT_IN_CAR, max_length=200)
    blacklist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderblackdriver', blank=True,
                                  null=True)

    price_nomi = models.CharField(max_length=200, blank=True, null=True)
    qayerdan_nomi = models.CharField(max_length=200, blank=True, null=True)
    qayerga_nomi = models.CharField(max_length=200, blank=True, null=True)

    driver_phone = models.CharField(max_length=200, blank=True, null=True)

    create_time = models.TimeField(default=datetime.now)
    create_date = models.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.qayerdan} => {self.qayerga}'

    def save(self, *args, **kwargs):
        self.qayerdan_nomi = self.qayerdan.nomi
        self.qayerga_nomi = self.qayerga.nomi
        self.price_nomi = self.price.narx
        if self.driver is not None:
            self.driver_phone = self.driver.phone
        else:
            self.driver_phone = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Faol Buyurtmalar'
        verbose_name_plural = 'Faol Buyurtmalar'


class ArchiveOrder(models.Model):
    STATUS = (
        ('yetkazildi', 'Yetkazildi'),
    )
    status = models.CharField(max_length=100, choices=STATUS, default='yetkazildi')
    qayerdan = models.CharField(max_length=1000)
    qayerga = models.CharField(max_length=1000)

    person_count = models.CharField(max_length=100, default=1)
    price = models.CharField(default=100000, max_length=200)

    client_phone = models.CharField(max_length=100)
    client_name = models.CharField(max_length=200)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archorder_customer')

    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archdriver', blank=True, null=True)

    create_time = models.TimeField(default=datetime.now)
    create_date = models.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.qayerdan} => {self.qayerga}'

    class Meta:
        verbose_name = 'Arxiv Buyurtmalar'
        verbose_name_plural = 'Arxiv Buyurtmalar'


class TempOrder(models.Model):
    STATUS = (
        ('yangi', 'Yangi'),
        ('olindi', 'Olindi')
    )

    PERSON_COUNT = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    )
    status = models.CharField(max_length=100, choices=STATUS, default='yangi')
    qayerdan = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tempqayerdanviloyat', null=True,
                                 blank=True)
    qayerga = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tempqayergadanviloyat', null=True,
                                blank=True)

    location = models.TextField(default='Manzil yo`q!')

    person_count = models.CharField(max_length=100, choices=PERSON_COUNT, default=1)
    price = models.ForeignKey(Price, on_delete=models.CASCADE, default='Kelishiladi', related_name='tempbuyurtmanarxi')

    client_phone = models.CharField(max_length=100)
    client_name = models.CharField(max_length=200)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temp_order_customer')

    create_time = models.TimeField(default=datetime.now)
    create_date = models.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.qayerdan} => {self.qayerga}'

    class Meta:
        verbose_name = 'Temp Buyurtmalar'
        verbose_name_plural = 'Temp Buyurtmalar'


class Filter(models.Model):
    STATUS = (
        ('barchasi', 'Barchasi'),
        ('filter', 'Filter'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='filterdriver')

    qayerdan = models.CharField(max_length=600, blank=True, null=True)
    qayerga = models.CharField(max_length=600, blank=True, null=True)

    status = models.CharField(max_length=200, choices=STATUS, default='barchasi')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Filterlar'
        verbose_name_plural = 'Filterlar'
