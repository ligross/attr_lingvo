import axios from 'axios'

let $axios = axios.create({
  baseURL: '/api/',
  timeout: 600000,
  headers: {'Content-Type': 'application/json'}
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token'
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {

  getResults (payload) {
    return $axios.post(`results/calculate`, payload)
      .then(response => response.data)
  }
}
