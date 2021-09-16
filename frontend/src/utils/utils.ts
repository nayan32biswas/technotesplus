export const totalPages = (count: any, limit: any): number => {
  if (!count || !limit) return 1;

  if (count && limit) {
    if (count <= limit) {
      return 1;
    }
    return Math.floor(count / limit) + (count % limit > 0 ? 1 : 0);
  } else {
    return 1;
  }
};
