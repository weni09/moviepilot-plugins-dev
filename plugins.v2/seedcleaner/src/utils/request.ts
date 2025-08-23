import axios from 'axios'
import session from './session'
const BASE_URL='http://192.168.1.121:3001/api/v1'
const USERNAME = 'admin'
const PASSWD = 'test123456'
// 创建 request 实例，支持 get/post/put/delete
const request = axios.create({
  baseURL: BASE_URL, // 设置基础路径
  timeout: 1200000, // 超时时间
})

const loginAndGetToken = async () => {
  const loginUrl = '/login/access-token'; // 登录接口路径
  const formData = new URLSearchParams();
  formData.append('username', USERNAME);
  formData.append('password', PASSWD);

  try {
    const response = await fetch(`${BASE_URL}${loginUrl}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        accept: 'application/json',
      },
      body: formData.toString(),
    });

    if (!response.ok) throw new Error('登录失败');

    const data = await response.json();
    const token = data.access_token;

    session.token = token; // 存入 session
    return token;
  } catch (error) {
    console.error('登录失败:', error);
    throw error;
  }
};


// 在请求拦截器中使用已获取的 token
request.interceptors.request.use(config => {
 const token = session.token
  if (token && !config.headers.Authorization) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// 添加响应拦截器（可选）
request.interceptors.response.use(response => {
  return response.data
}, error => {
  console.error('API 请求失败:', error)
  return Promise.reject(error)
})


export {loginAndGetToken, request}