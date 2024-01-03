export const subString = string => {
  if (string && string.length) {
    return string.split(' ').slice(0, 8).join(' ');
  }
  return string;
};
