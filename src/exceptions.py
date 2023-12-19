# GLOBAL
NO_DATA_FOUND = "No data found."
NO_RECORD = "Record not found."
SERVER_ERROR = "Server error has occurred."
SUCCESS_DELETE = "Record with id: `%s` was successfully deleted."
INVALID_PHONE = "Invalid phone number. Please ensure your phone number contains only digits and the symbols +()-, and is between 10 and 20 characters in length."
INVALID_PHOTO = "Unsupported media type: %s. Supported types: %s"
OVERSIZE_FILE = "File size exceeds the maximum allowed size (3MB)"

# DEPARTMENTS
DEPARTMENTS_EXISTS = "Department with name: `%s` already exists in the database."
SUB_DEP_EXISTS = "Sub Department `%s` for Main Department %s already exists."
SUCCESS_CREATE = "Successfully created Sub Department: %s for Main Department %s."
CREATE_MAIN = "Successfully created Main Department: %s."
EXISTS_MAIN = "Main Department `%s` already exists."
NO_SUB_DEPARTMENT = "No sub-departments found for this department."
NO_MEDIA = "Media for this sub-department not found."
DELETE_ERROR = "Cannot delete the last sub-department of a main department."

# CONTACTS
CONTACTS_SUCCESS_CREATE = "Contacts have been created successfully."
CONTACTS_ALREADY_EXISTS = "Contacts already exists."
INVALID_FIELD = "Invalid field name."

# USER
EMAIL_BODY = """
Вітаємо!

Ви отримали цього листа, тому що зробили запит на відновлення паролю для вашого облікового запису в панелі керування Art School.

Для відновлення паролю, будь ласка, перейдіть за наступним посиланням:
https://art-school-frontend.vercel.app/login/password-recovery/%s

Якщо ви не робили запит на відновлення паролю, просто проігноруйте це повідомлення.

З повагою,
Команда Art School
"""
USER_EXISTS = "User %s already exists."
AFTER_REGISTER = "User %s has registered."
AFTER_LOGIN = "You have successfully logged in."
PASSWORD_LEN_ERROR = "Password should be at least 8 characters."
PASSWORD_UNIQUE_ERROR = "Password should not contain e-mail."
PASSWORD_STRENGTH_ERROR = "Password must contain a lowercase letter, uppercase letter, a number and a special symbol."
PASSWORD_CHANGE_SUCCESS = "The password has been changed."
PASSWORD_NOT_MATCH = "New passwords do not match."
OLD_PASS_INCORRECT = "Old password is incorrect."

# SCHOOL ADMINISTRATION
PERSON_EXISTS = "Administrator with name %s already exists in the database."
SUCCESS = "Administrator %s create successfuly."

# GALLERY
GALLERY_PINNED_EXISTS = "Media with position number: `%s` already exists."
GALLERY_IS_NOT_A_VIDEO = "The selected recording is not a video"
GALLERY_IS_NOT_A_PHOTO = "The selected recording is not a photo"
INVALID_DEPARTMENT = "SubDepartment with id %s not found."
