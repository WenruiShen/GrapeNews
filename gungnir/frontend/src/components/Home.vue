<template>
  <div id="homepage">
    <app-headline></app-headline>
    <app-trending></app-trending>
    <app-footer></app-footer>

  </div>
</template>

<script>
  import Headline from './Headlines.vue'
  import Trending from './Trending.vue'
  import Footer from './Footer.vue'
  export default{
    components: {
      'app-headline': Headline,
      'app-trending': Trending,
      'app-footer': Footer
    }
  }
</script>

<style scoped>

</style>

