from sqladmin import ModelView

from src.contacts.models import Contact


class ContactsView(ModelView, model=Contact):
    column_list = [Contact.id, Contact.address, Contact.email]
