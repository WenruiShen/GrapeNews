<template>
  <div id="slide">

    <div class="container">
      <img v-if="isLoading" src="https://media.giphy.com/media/8l3nG5DahWaYg/giphy.gif">

      <slider style="width: auto; height: 400px ">
        <slider-item v-for="(topic, index) in topics" :key="index">
          <router-link :to="{ name: 'Timeline' , params: { topicId: topic.id }}">
            <img :src="topic.image_url" class="img-responsive">
          </router-link>
          <div class="carousel-caption" alt="no image here">
            <h3>{{topic.news_title}}</h3>
          </div>
        </slider-item>
      </slider>
    </div>
  </div>
</template>

<script>
  import {Slider, SliderItem} from 'vue-easy-slider'
  import Vue from 'vue'

  export default{
    el: 'body',
    data () {
      return {
        topics: [],
        isLoading: true
      }
    },
    created: function () {
      this.$axios.get('/topics_latest/3-0.json')
        .then(response => {
          this.topics = response.data
          this.topics.forEach(topic => {
            this.$axios.get('/topic/' + topic.id + '/news_latest/1.json')
              .then(response => {
                Vue.set(topic, 'news_title', response.data[0].news_title)
                Vue.set(topic, 'news_url', response.data[0].news_url)
                Vue.set(topic, 'image_url',
                  (response.data[0].image_url.length === 0 ? 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg' : response.data[0].image_url))
              })
          })
          this.isLoading = false
//          console.log(this.topics)
        })
        .catch(e => {
          this.errors.push(e)
          console.log(this.errors)
        })
    },
    components: {
      Slider,
      SliderItem
    }
  }
</script>

<style scoped>

  .container {
    width: 70%;
    margin: 5px auto;
    margin-top: 5%;
    margin-bottom: 3%;
  }

  img {
    width: auto;
    height: 400px;
    min-height: 100%;
    min-width: 100%;
  }

  h3 {
    font-weight: bold;
    font-size: 48px;
  }

  .carousel-caption {
    height: 100px;
    bottom: 0;
    padding-top: 0;
    padding-bottom: 20px;
    width: inherit;
    right: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.7);
    opacity: 0.9;
  }

  h3 {
    font-size: 30px;
    font-weight: bold;
  }
</style>
