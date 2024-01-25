from dataclasses import dataclass

from payments.models import Requisite


@dataclass
class TableHeader:
    verbose_name: str
    name: str


def get_requisite_table_headers():
    return [
        TableHeader('Номер реквизита', 'id'),
        TableHeader('Тип платежа', 'payment_type'),
        TableHeader('Тип карты/счета', 'card_or_account_type'),
        TableHeader('ФИО', 'full_name'),
        TableHeader('Номер телефона', 'phone'),
        TableHeader('Лимит', 'limit'),
    ]


def get_requisite_model_fields() -> list[str]:
    field_names = [field.name for field in Requisite._meta.get_fields()]
    return field_names
