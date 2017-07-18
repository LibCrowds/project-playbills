import axios from 'axios'

export const api = axios.create({
  baseURL: `${process.env.API_URL}`,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000,
  data: {}  // Must always be set otherwise Content-Type gets deleted
})
