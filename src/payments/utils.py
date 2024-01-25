from dataclasses import dataclass


@dataclass
class TableHeader:
    name: str
    ordering: str


def get_requisite_table_headers():
    return [
        TableHeader('Номер реквизита', 'id'),
        TableHeader('Тип платежа', 'payment_type'),
        TableHeader('Тип карты/счета', 'card_or_account_type'),
        TableHeader('ФИО', 'full_name'),
        TableHeader('Номер телефона', 'phone'),
        TableHeader('Лимит', 'limit'),
    ]
