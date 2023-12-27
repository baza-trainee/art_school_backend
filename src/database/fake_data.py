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
        "description": "Духові та ударні музичні інструменти вважаються одними із найдавніших у світі. Вони відігравали важливу роль у культурі різних народів та цивілізацій. Духові та ударні інструменти є обов'язковою складовою частиною симфонічних, багатьох камерних та народних оркестрів, основою духових та джазових оркестрів!На відділі духових та ударних інструментів працюють справжні професіонали викладачі. Вони передають свій досвід маленьким музикантам. У нас дуже дружній колектив та яскраве творче життя. Чекаємо в нашій родині!",
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Народний відділ",
        "description": "Українські народні інструменти мають довгу та багату історію, яка сягає часів Київської Русі. Вони є важливим елементом української культури та традиції, а гра на народних інструментах є способом збереження та передачі цієї спадщини наступним поколінням. Українські народні інструменти мають унікальний звук. Цей звук є результатом використання різних матеріалів та методів їх виготовлення. Гра на народних інструментах є способом виразити свою музичність та творчість. Українські народні інструменти порівняно доступні, що робить їх привабливими для людей різного достатку. Це сприяє збереженню та популяризації народної музики та інструментів.",
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Теоретичний відділ",
        "description": desc,
        "main_department_id": 1,
    },
    {
        "sub_department_name": "Джазовий відділ",
        "description": """Джазове відділення Київської Дитячої Школи Мистецтв №2 запрошує до навчання діточок охочих співати та грати на різних музичних інструментах!
                            Індивідуальні та групові заняття з професійними викладачами допоможуть молоді відчинити двері у яскравий світ музики, зробити перші кроки у виконавській майстерності, імпровізації та розвитку своїх музичних талантів.

                            До вашої уваги навчання за фахом:
                            - Джазовий вокал
                            - Фортепіано 
                            - Електро та акустична гітари
                            - Бас гітара
                            - Барабани

                            Що ми пропонуємо:
                            - Очна форма навчання та індивідуальні уроки з 
                            найкращими викладачами Києва.
                            - Сучасне, обладнане та комфортне творче середовище для вашої дитини. 
                            - Зручне розташування у історичному центрі міста.
                            Пільги для певних категорій сімей (затверджені державою)
                            - навчання за бюджетною программою також включає заняття на додатковому музичному інтструменті та відвідування теоретичних дисциплін. 

                            Увага:
                            Навчальний процес відбувається у дружній та теплій атмосфері!
                            """,
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
        "description": """Хор – це колектив співаків, які виконують разом один твір із супроводом, або ж a cappella (без супроводу). Хор – це не лише про спів, а й про спілкування, вміння слухати один одного, працювати в ансамблі. Наше головне  завдання - залюбити вас у Пісню, відчути, як вона бринить всередині нас. Ми вчимось дотримуватись дисципліни; організовано виконувати вказівки хормейстера (керівник колективу); проявляти себе, як артист.
 На нашому відділі творять мистецтво Хор хлопчиків «Менестрелі» та Дівочий хор, який поділяється на старший склад хору «DOraDO» (свою назву хор запозичив у сузір'ї південного неба Золота Рибка (Doradus), та молодший склад хору «SoleMio».
 Наші хорові колективи є лауреатами всеукраїнських та міжнародних конкурсів, та фестивалів в Угорщині, Естонії, Чехії. Ведемо активну, багаторічну концертну діяльність. У репертуарі колективу обробки українських народних пісень, твори українських та зарубіжних композиторів. 
 Разом з учасниками й керівниками наших хорів, та концертмейстерами – ми рухаємось до гармонії, не тільки в музиці, а й в колективі.
""",
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ сольного співу",
        "description": "Спів – один з найбільш доступних і зрозумілих для дитини видів музичного мистецтва. Заняття вокалом розвивають не лише слух, голос та почуття ритму. Спів позитивно впливає на фізичний розвиток дітей, адже правильне дихання під час виконання пісень забезпечує повноцінне постачання організму киснем, що благотворно впливає на роботу серцево-судинної системи. А у процесі навчання вокалу здійснюється робота над дикцією, що допомагає запобігти або позбавитися від заїкання і гаркавості. Спів не тільки впливає на розвиток дітей, а й дає їм можливість висловити свої почуття. Дитина стане впевненішою в собі Розвине музичний слух і буде «потрапляти в ноти» вже з перших уроків Розкриє свій природний тембр голосу Покращиться дикція та почуття ритму Навчиться працювати з мікрофоном та монітором Напрацює репертуар, отримає перший досвід виступів і перемог у конкурсах. ",
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ естрадного вокалу",
        "description": """Голос - універсальний інструмент, який завжди можна взяти з собою. А ще - це один із проявів унікальності кожної людини, адже, попри усі об'єднувальні фактори, кожен голос - неповторний.
На відділі Естрадного співу ми вчимося керувати власним голосом, розвиваємо його самобутність і силу. 
Ми формуємо чітку дикцію, працюємо над артистичністю, акторською майстерністю, допомагаючи нашим вихованцям стати не зірками великої сцени, ні - більше: впевненими й гармонійними особистостями, здатними до комунікації, незалежно від будь-яких зовнішніх факторів.
""",
        "main_department_id": 2,
    },
    {
        "sub_department_name": "Відділ народного співу",
        "description": """Цікаво відзначити той факт, що спів одночасно діє на різні сторони нашої
особистості й незалежно від віку сприяє виробленню енергії, що є
рушійною силою емоційного та психофізичного розвитку. А значить, спів
гармонійно й всебічно впливає на розвиток людини в цілому.
 
Мета навчання полягає у залученні учнів до української та світової
музичної культури засобами пісенної творчості, формуванні
національного самоусвідомлення та вихованні любові до Батьківщини.
На відділі є два вокальних ансамблі:
«Веселад» - ансамбль академічної народної пісні.
«Первоцвіт» - фольклорний ансамбль.""",
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
        "sub_department_name": "Відділ Театрального відділення",
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
        "sub_department_name": "Дошкільний та підготовчий відділ",
        "description": """Дошкільна освіта є невід`ємною частиною у системі безперервного навчання.
Дошкільний відділ КДШМ № 2 ім. М.І. Вериківського проводить набір дітей віком від 1року до 6 років.
 Основні завдання : ознайомлення з основними видами мистецтв, надання  можливості дитині спробувати себе у різноманітній творчій діяльності, підготовка дітей до загальноосвітньої школи та школи мистецтв.
 Розроблений навчальний план включає в себе естетичний комплекс (музика, хореографія, оразотворче мистецтво) і загальноосвітній цикл (читання, математика, англійська мова).
 Дітям шести років пропонуємо курс інтенсивної підготовки до школи з повним естетичним циклом)
 Педагоги дошкільного відділу - це талановиті творчі люди з багатим досвідом та великим багажем знань. 
 Розвиваймо обдаровану дитину разом!
""",
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
