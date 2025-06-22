// src/utils/auth/session.ts

const TOKEN_KEY = 'auth_token';

 const session = {
  // 获取 token
  get token(): string | null {
    return sessionStorage.getItem(TOKEN_KEY);
  },

  // 设置 token
  set token(token: string | null) {
    if (token) {
      sessionStorage.setItem(TOKEN_KEY, token);
    } else {
      sessionStorage.removeItem(TOKEN_KEY);
    }
  },

  // 清除 token
  clear() {
    sessionStorage.removeItem(TOKEN_KEY);
  },
};

export default session;