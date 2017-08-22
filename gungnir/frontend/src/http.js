import axios from 'axios'
import store from './store/store'
import router from './router/index'

// axios settings
axios.defaults.timeout = 5000

// axios.defaults.baseURL = 'http://csi6220-2-vm2.ucd.ie/api'
// axios.defaults.baseURL = 'http://localhost:8000/api'
axios.defaults.baseURL = 'http://' + window.location.host + '/api'

// http request interceptor
axios.interceptors.request.use(
  config => {
    if (localStorage.token) {
      config.headers.Authorization = `token ${localStorage.token}`
    }
    return config
  },
  err => {
    return Promise.reject(err)
  })

// http response interceptor
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 401 clean token & redirect
          store.commit('logout')
          router.push('/')
      }
    }
    // console.log(JSON.stringify(error));//console : Error: Request failed with status code 402
    return Promise.reject(error.response.data)
  })

export default axios
