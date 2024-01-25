from dataclasses import dataclass

from payments.models import Requisite


@dataclass
class TableHeader:
    verbose_name: str
    name: str
    column_size: str


def get_requisite_table_headers():
    return [
        TableHeader('Номер реквизита', 'id', '5%'),
        TableHeader('Тип платежа', 'payment_type', '10%'),
        TableHeader('Тип карты/счета', 'card_or_account_type', '15%'),
        TableHeader('ФИО', 'full_name', '45%'),
        TableHeader('Номер телефона', 'phone', '15%'),
        TableHeader('Лимит', 'limit', '10%'),
    ]


def get_requisite_model_fields() -> list[str]:
    field_names = [field.name for field in Requisite._meta.get_fields()]
    return field_names
