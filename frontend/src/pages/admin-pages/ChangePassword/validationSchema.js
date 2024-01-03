import * as Yup from 'yup';

export const validatePassword = value => {
  let errors = [];
  if (!/[a-z]/.test(value)) {
    errors.push('маленьку літеру');
  }
  if (!/[A-Z]/.test(value)) {
    errors.push('велику літеру');
  }
  if (!/\d/.test(value)) {
    errors.push('цифру');
  }
  if (!/[@#$%^&+=!]/.test(value)) {
    errors.push('спеціальний символ');
  }
  return `Пароль повинен містити ${errors.join(', ')}`;
};

export const passwordValidation = Yup.object().shape({
  oldPassword: Yup.string()
    .min(8, 'Мінімальна довжина назви 8 символи')
    .required('введіть попередній пароль'),
  newPassword: Yup.string()
    .min(8, 'Мінімальна довжина назви 8 символи')
    .max(64, 'Максимальна довжина 64 символи')
    .required('введіть новий пароль')
    .matches(/^(?=.*[a-z])/, 'Повинен містити  хоча б одну маленьку літеру')
    .matches(/^(?=.*[A-Z])/, 'Повинен містити хоча б  одну велику літеру')
    .matches(/^(?=.*[0-9])/, 'Повинен містити хоча б  одну цифру')
    .matches(
      /^(?=.*[@#$%^&+=!])/,
      'Повинен містити хоча б  один спеціальний символ  @ # $ % ^ & + = !'
    ),
  confirmPassword: Yup.string().oneOf(
    [Yup.ref('newPassword')],
    'Паролі не співпадають'
  ),
});
