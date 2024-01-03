import { useEffect } from 'react';
import useContactsStore from '@/store/contactsStore';
import PageTitle from '@/components/admin-components/PageTitle/PageTitle';
import ContactsTable from '@/components/admin-components/Сontacts/ContactsTable/ContactsTable';
import BreadCrumbs from '@/components/admin-components/BreadCrumbs/BreadCrumbs';
import SpinnerAdmin from '@/components/admin-components/SpinnerAdmin/SpinnerAdmin';
import PlaceholderAdmin from '@/components/admin-components/PlaceholderAdmin/PlaceholderAdmin';

const breadcrumbs = ['Контакти'];

const ContactsPageAdmin = () => {
  const { getContacts } = useContactsStore();
  const contacts = useContactsStore(state => state.contacts);
  const loading = useContactsStore(state => state.loading);
  const error = useContactsStore(state => state.error);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await getContacts();
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [getContacts]);

  return (
    <div>
      <BreadCrumbs breadcrumbs={breadcrumbs} />
      <PageTitle
        title="Контакти"
        showBackButton={false}
        showActionButton={false}
      />
      {loading && !Object.keys(error).length ? (
        <SpinnerAdmin />
      ) : (
        <ContactsTable data={contacts} />
      )}
      {error && Object.keys(error).length ? <PlaceholderAdmin /> : null}
    </div>
  );
};

export default ContactsPageAdmin;
