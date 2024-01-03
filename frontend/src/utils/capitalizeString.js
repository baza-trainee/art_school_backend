export const capitalizeString = string => {
  const splittedString = string.split('');
  return `${splittedString[0].toUpperCase()}${splittedString
    .slice(1)
    .join('')}`;
};
