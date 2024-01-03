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

export const newsValidation = Yup.object().shape({
  title: Yup.string()
    .min(2, 'Мінімальна довжина назви 2 символи')
    .max(120, 'Максимальна довжина назви 120 символів')
    .matches(
      /^[a-zA-Zа-яА-ЯҐґЄєІіЇї\s\d'’`.,:;"()!?-]+$/,
      'Введіть коректну назву'
    ),
  text: Yup.string()
    .min(2, 'Мінімальна довжина тексту 2 символи')
    .max(2000, 'Максимальна довжина тексту 2000 символів')
    .matches(
      /^[a-zA-Zа-яА-ЯҐґЄєІіЇї\s\d'’`.,:;"()?!-]+$/,
      'Введіть коректний текст'
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
});
