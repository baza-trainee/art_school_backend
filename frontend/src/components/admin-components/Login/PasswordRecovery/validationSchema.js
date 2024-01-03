import * as Yup from 'yup';

export const recoveryValidation = Yup.object().shape({
  email: Yup.string()
    .required('Поле не може бути пустим')
    .min(6, 'електронна адреса має бути мінімум 6 символів')
    .max(20, 'електронна адреса має бути максимум 20 символів')
    .matches(
      /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
      'Введіть коректну електронну адресу'
    ),
});
