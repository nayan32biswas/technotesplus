export const HOST: string =
  process.env.VUE_APP_DEVHOST || "http://localhost:8000";

export const API_ROOT = `${HOST}/api`;

export const SIGNUP_URL = `${API_ROOT}/signup/`;
export const LOGIN_URL = `${API_ROOT}/login/`;
export const LOGOUT_URL = `${API_ROOT}/logout/`;
export const REFRESH_URL = `${API_ROOT}/refresh-token/`;
export const PROFILE_URL = `${API_ROOT}/me/`;
export const USERS_URL = `${API_ROOT}/users/`;
export const CHANGE_PASSWORD_URL = `${API_ROOT}/password/password_reset/`;

export const NOTE_URL = `${API_ROOT}/note/`;
export const NOTE_DETAIL_URL = (slug: string): string =>
  `${API_ROOT}/note/${slug}/`;
export const SHARE_NOTE_URL = `${API_ROOT}/share-note/`;
export const SHARE_NOTE_DETAIL_URL = (slug: string): string =>
  `${API_ROOT}/share-note/${slug}/`;
