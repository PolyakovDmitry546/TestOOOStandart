from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Requisite(models.Model):
    """Модель платежных реквизитов"""
    CARD = 'CARD'
    ACCOUNT = 'ACCOUNT'
    PAYMENT_TYPE = {
        CARD: 'Карта',
        ACCOUNT: 'Платежный счет'
    }

    payment_type = models.CharField(
        max_length=7,
        choices=PAYMENT_TYPE,
        verbose_name='Тип платежа'
    )
    card_or_account_type = models.CharField(
        max_length=30,
        verbose_name='Тип карты/счета'
    )
    full_name = models.CharField(max_length=255, verbose_name='ФИО владельца')
    phone = PhoneNumberField(verbose_name='Номер телефона')
    limit = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        verbose_name='Лимит'
    )

    class Meta:
        db_table = 'requisites'
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'


class Invoice(models.Model):
    """Модель заявок на оплату"""
    AWAITING_PAYMENT = 'AWAITING_PAYMENT'
    PAID = 'PAID'
    CANCELED = 'CANCELED'
    INVOICE_STATUS = {
        AWAITING_PAYMENT: 'Ожидает оплаты',
        PAID: 'Оплачена',
        CANCELED: 'Отменена'
    }

    amount = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        verbose_name='Сумма заявки'
    )
    requisite = models.ForeignKey(
        to=Requisite,
        on_delete=models.PROTECT,
        verbose_name='Реквизиты заявки'
    )
    status = models.CharField(
        max_length=16,
        choices=INVOICE_STATUS,
        verbose_name='Статус заявки'
    )

    class Meta:
        db_table = 'invoices'
        verbose_name = 'Заявка на оплату'
        verbose_name_plural = 'Заявки на оплату'
