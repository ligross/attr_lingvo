import axios from 'axios'

let $axios = axios.create({
  baseURL: '/api/',
  timeout: 900000,
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

  calculateResults (payload) {
    return $axios.post(`results/calculate`, payload)
      .then(response => {
        console.log(response.data)
        return response.data
      }
      )
  },
  recalculateResults (payload) {
    return $axios.post(`results/recalculate`, payload)
      .then(response => {
        console.log(response.data)
        return response.data
      }
      )
  }
}
