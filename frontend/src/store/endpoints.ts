export const HOST: string =
  process.env.VUE_APP_DEVHOST || "http://localhost:8000";

export const API_ROOT = `${HOST}/api`;

const ACCOUNT = `${API_ROOT}/account`;
export const LOGIN_URL = `${ACCOUNT}/login/`;
export const LOGOUT_URL = `${ACCOUNT}/logout/`;
export const SIGNUP_URL = `${ACCOUNT}/signup/`;
export const REFRESH_URL = `${ACCOUNT}/refresh-token/`;
export const PROFILE_URL = `${ACCOUNT}/me/`;
