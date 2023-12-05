from faker import Faker


faker = Faker()
desc = faker.text()

DEPARTMENTS = [
    "Музичне відділення",
    "Вокально-хорове відділення",
    "Хореографічне відділення",
    "Театральне відділення",
    "Образотворче відділення",
    "Дошкільне та підготовче відділення",
]
SUB_DEPARTMENTS = [
    # Музичне відділення
    {
        "sub_department_name": "Струнний відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Духовий відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Народний відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Теоретичний відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Джазовий відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Відділ спеціалізованого та загального фортепіано",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Відділ концертмейстрів",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Відділ камерного ансамблю",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Історія мистецтв",
        "description": desc,
        "main_department_id": 1,
    },
    # Вокально-хорове відділення
    {
        "sub_department_name": "Хоровий відділ",
        "description": desc,
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ сольного співу",
        "description": desc,
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ естрадного вокалу",
        "description": desc,
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ народного співу",
        "description": desc,
        "main_department_id": 2,
    },
    # Хореографічне відділення
    {
        "sub_department_name": "Відділ класичного танцю",
        "description": desc,
        "main_department_id": 3,
    },
    {
        "sub_department_name": "Відділ народного танцю",
        "description": desc,
        "main_department_id": 3,
    },
    {
        "sub_department_name": "Відділ сучасного танцю",
        "description": desc,
        "main_department_id": 3,
    },
    # Театральне відділення
    {
        "sub_department_name": "Псевдо відділ Театрального відділення",
        "description": desc,
        "main_department_id": 4,
    },
    # Образотворче відділення
    {
        "sub_department_name": "Розвиток образотворчої уяви та мислення 1-4 класи",
        "description": desc,
        "main_department_id": 5,
    },
    {
        "sub_department_name": "Живопис 4-7 класи",
        "description": desc,
        "main_department_id": 5,
    },
    {
        "sub_department_name": "Дизайнерсько-графічний напрямок 4-7 класи",
        "description": desc,
        "main_department_id": 5,
    },
    # Дошкільне та підготовче відділення
    {
        "sub_department_name": "Псевдо відділ Дошкільного та підготовчого відділення",
        "description": desc,
        "main_department_id": 6,
    },
]
CONTACTS = {"address": "вул.Бульварно-Кудрявська, 2", "phone": "+38(097)290-79-40"}

SLIDES = [
    {
        "title": "Slide1",
        "description": "Slide1 Test description",
    },
    {
        "title": " Slide2",
        "description": "Slide2 Test description",
    },
]
ADMINISTRATIONS = [
    {
        "full_name": "Ірина Коваленко",
        "position": "Заступник директора",
        "photo": "http://res.cloudinary.com/dmfaqrftb/image/upload/v1701766157/static/SchoolAdministration/pvm8ad5krib3dzxlvsdk.jpg",
    },
    {
        "full_name": "Микола Литвиненко",
        "position": "Консьєрж",
        "photo": "http://res.cloudinary.com/dmfaqrftb/image/upload/v1701766221/static/SchoolAdministration/avrrwy3mke4slpqzk0ft.jpg",
    },
    {
        "full_name": "Василь Петренко",
        "position": "Головний бухгалтер",
        "photo": "http://res.cloudinary.com/dmfaqrftb/image/upload/v1701766264/static/SchoolAdministration/zdcn16zrdv5ofmkqsp26.jpg",
    },
    {
        "full_name": "Наталія Сидоренко",
        "position": "Секретар",
        "photo": "http://res.cloudinary.com/dmfaqrftb/image/upload/v1701766307/static/SchoolAdministration/eeh6t0smicriaesvdqlq.jpg",
    },
    {
        "full_name": "Олександр Шевченко",
        "position": "Директор",
        "photo": "http://res.cloudinary.com/dmfaqrftb/image/upload/v1701766646/static/SchoolAdministration/y8ovyujmirsluary2pxp.jpg",
    },
]
