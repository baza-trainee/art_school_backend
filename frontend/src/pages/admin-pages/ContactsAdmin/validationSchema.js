import * as Yup from 'yup';
import { URL, YOUTUBE_URL, FACEBOOK_URL } from '@/utils/regex';

export const contactsValidation = Yup.object().shape({
  map_url: Yup.string()
    .min(2, 'Мінімальна довжина назви 2 символи')
    .max(120, 'Максимальна довжина назви 120 символів')
    .matches(
      /^https:\/\/maps\.app\.goo\.gl\/[A-Za-z0-9]+$/,
      'Введіть коректний лінк до Google Maps'
    ),

  address: Yup.string()
    .min(5, 'Мінімальна довжина поля 5 символів')
    .max(50, 'Максимальна довжина поля 50 символів'),

  phone: Yup.string().matches(
    /^\+?[0-9\s()-]{8,}$/,
    'Введіть коректний номер телефону'
  ),

  email: Yup.string()
    .min(5, 'Мінімальна довжина поля 5 символів')
    .max(35, 'Максимальна довжина поля 35 символів')
    .matches(
      /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
      'Введіть коректну електронну адресу'
    ),

  facebook_url: Yup.string()
    .min(5, 'Мінімальна довжина поля 5 символів')
    .max(50, 'Максимальна довжина поля 50 символів')
    .matches(FACEBOOK_URL, 'Введіть коректну електронну адресу Facebook'),

  youtube_url: Yup.string()
    .min(5, 'Мінімальна довжина поля 5 символів')
    .max(50, 'Максимальна довжина поля 50 символів')
    .matches(YOUTUBE_URL, 'Введіть коректну електронну адресу Youtube'),

  admission_info_url: Yup.string()
    .min(5, 'Мінімальна довжина поля 5 символів')
    .max(50, 'Максимальна довжина поля 50 символів')
    .matches(URL, 'Введіть коректну електронну адресу'),

  statute_url: Yup.string()
    .min(5, 'Мінімальна довжина поля 5 символів')
    .max(50, 'Максимальна довжина поля 50 символів')
    .matches(URL, 'Введіть коректну електронну адресу'),

  legal_info_url: Yup.string()
    .min(5, 'Мінімальна довжина поля 5 символів')
    .max(50, 'Максимальна довжина поля 50 символів')
    .matches(URL, 'Введіть коректну електронну адресу'),
});
