export const isDataValid = data => {
  const isValid = !Array.from(data).flat().includes('undefined');
  return isValid;
};
