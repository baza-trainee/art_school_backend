import * as Yup from 'yup';
import { formatBytes } from '@/utils/formatBytes';

const sizeLimit = 1024 * 1024 * 3;

const fileTypes = [
  'image/jpg',
  'image/jpeg',
  'image/png',
  'image/webp',
  'for-url',
];

function isValidFileType(fileType) {
  return fileTypes.includes(fileType);
}

export const achievementsValidation = Yup.object().shape({
  description: Yup.string()
    .required('Введіть опис досягнення')
    .min(2)
    .max(120)
    .matches(
      /^[a-zA-Zа-яА-ЯҐґЄєІіЇї\s\d'’.,:;"()!?-]+$/,
      'Введіть коректний опис'
    ),
    image: Yup.mixed()
    .test('is-value', 'Додайте зображення', value => value && value.length > 0)
    .test('is-image-from-db', 'Додайте зображення', value => {
      value && value[0]?.size === 0 && value[0]?.type === 'for-url';
      return true;
    })
    .test(
      'is-valid-type',
      'Зображення має бути в форматі .jpg, .png або .webp',
      value => isValidFileType(value && value[0]?.type)
    )
    .test(
      'is-valid-size',
      `Максимальний розмір зображення ${formatBytes(sizeLimit)}`,
      value => value && value[0]?.size <= sizeLimit
    ),
    pinned_position: Yup.mixed(),
});

export const galleryValidation = Yup.object().shape({
  description: Yup.string()
    .required('Введіть опис досягнення')
    .min(2)
    .max(150)
    .matches(
      /^[a-zA-Zа-яА-ЯҐґЄєІіЇї\s\d'’.,:;"()!?-]+$/,
      'Введіть коректний опис'
    ),
    image: Yup.mixed()
    .test('is-value', 'Додайте зображення', value => value && value.length > 0)
    .test('is-image-from-db', 'Додайте зображення', value => {
      value && value[0]?.size === 0 && value[0]?.type === 'for-url';
      return true;
    })
    .test(
      'is-valid-type',
      'Зображення має бути в форматі .jpg, .png або .webp',
      value => isValidFileType(value && value[0]?.type)
    )
    .test(
      'is-valid-size',
      `Максимальний розмір зображення ${formatBytes(sizeLimit)}`,
      value => value && value[0]?.size <= sizeLimit
    ),
    pinned_position: Yup.mixed(),
});

