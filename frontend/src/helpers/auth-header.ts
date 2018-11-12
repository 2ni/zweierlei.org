export function authHeader() {
  const user = JSON.parse((localStorage as any).getItem('user'));

  if (user && user.token) {
    return { Authorization: 'Bearer ' + user.token };
  } else {
    return {};
  }
}
