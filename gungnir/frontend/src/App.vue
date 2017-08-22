<template>
  <div id="app">
    <app-navi></app-navi>

    <router-view></router-view>
  </div>
</template>

<script>
  import navi from './components/Navigation.vue'
  export default {
    name: 'app',
    components: {
      'app-navi': navi
    },
    created () {
      if (localStorage.token) {
        this.$axios.get('/users/details/')
          .then(response => {
            console.log(response)
            this.$store.commit('login', {token: localStorage.token, user_data: response.data})
          })
          .catch(err => console.log(err))
      }
    }
  }

</script>

<style>
#app {
  background-image: radial-gradient(73% 147%, #EADFDF 59%, #ECE2DF 100%), radial-gradient(91% 146%, rgba(255, 255, 255, 0.50) 47%, rgba(0, 0, 0, 0.50) 100%);
  background-blend-mode: screen;
}


</style>
