from sqladmin import ModelView

from src.contacts.models import Contacts


class ContactsView(ModelView, model=Contacts):
    column_list = [Contacts.id, Contacts.address, Contacts.email]
