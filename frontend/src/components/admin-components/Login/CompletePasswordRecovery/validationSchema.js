import * as Yup from 'yup';

export const completeRecoveryValidation = Yup.object().shape({
  password: Yup.string()
    .required('ВВедіть пароль')
    .min(8, 'Пароль має бути мінімум 8 символів')
    .max(64, 'Пароль має бути максимум 64 символи')
    .matches(/^(?=.*[a-z])/, 'Повинен містити  хоча б одну маленьку літеру')
    .matches(/^(?=.*[A-Z])/, 'Повинен містити хоча б  одну велику літеру')
    .matches(/^(?=.*[0-9])/, 'Повинен містити хоча б  одну цифру')
    .matches(
      /^(?=.*[@#$%^&+=!])/,
      'Повинен містити хоча б  один спеціальний символ  @ # $ % ^ & + = !'
    ),
  confirm_password: Yup.string().test(
    'passwords-match',
    'Passwords must match',
    function (value) {
      return this.parent.password === value;
    }
  ),
});
