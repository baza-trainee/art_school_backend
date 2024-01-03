export const formatDate = dateString => {
  const inputDate = new Date(dateString);

  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  };

  const locale = 'uk-UK';

  const formattedDate = inputDate
    .toLocaleString(locale, options)
    .split(' ')
    .slice(0, 3)
    .join(' ');

  return formattedDate;
};
