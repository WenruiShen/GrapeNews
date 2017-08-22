import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    token: ''
  },
  getters: {
    hasLogin: state => {
      return state.user !== null
    },
    user: state => {
      return state.user
    },
    username: state => {
      return state.user['username']
    },
    fname: state => {
      return state.user['first_name']
    },
    lname: state => {
      return state.user['last_name']
    },
    userSubscribeTopic: state => {
      return state.user['collection_topic_id_array']
    }
  },
  mutations: {
    signup (state, payload) {
      state.user = payload.user_data
      // state.token = payload.token
      localStorage.token = payload.token
    },
    login (state, payload) {
      state.user = payload.user_data
      // state.token = payload.token
      localStorage.token = payload.token
    },
    logout (state) {
      state.user = null
      localStorage.removeItem('token')
    },
    update (state, payload) {
      state.user['first_name'] = payload['first_name']
      state.user['last_name'] = payload['last_name']
      state.user['collection_topic_id_array'] = payload['collection_topic_id_array']
    }
  }
})
