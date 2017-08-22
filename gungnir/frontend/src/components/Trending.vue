<template>
  <div id="topics">
    <div class="container">
      <div v-infinite-scroll="loadMore" infinite-scroll-disabled="busy" infinite-scroll-distance="10">
        <div class="row row-offcanvas row-offcanvas-right">
          <div class="col-md" v-for="topic in topics">
            <div class="card">
              <router-link :to="{ name: 'Timeline', params:{ topicId: topic.id }}">
                <img class="card-img-top" :src="topic.image_url" alt="no image here">
              </router-link>
              <div class="card-block">
                <h4 id="1" class="card-title">{{ topic.topic_name }}</h4>
                <p class="card-text">{{ topic.news_title }}</p>
                <span v-if="hasLogin">
                  <a class="glyphicon glyphicon-heart-empty" v-if="!checkSubscribe(topic.id)"
                     @click="subscribe(topic.id)"></a>
                  <a class="glyphicon glyphicon-heart" v-if="checkSubscribe(topic.id)"
                     @click="unsubscribe(topic.id)"></a>
                </span>
                <a :href="topic.news_url" class="glyphicon glyphicon-link"></a>
                <small>{{ topic.news_date }}</small>
              </div>
            </div>
          </div>
        </div>
        <div style="text-align: center"><p style="display: inline-block">{{ limit }}</p></div>
      </div>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import infiniteScroll from 'vue-infinite-scroll'

  export default{
    data () {
      return {
        topics: [],
        tempTopics: [],
        errors: [],
        isloading: false,
        counter: 0,
        limit: '',
        collection: [],
        busy: false
      }
    },
    computed: {
      user () {
        return this.$store.getters.user
      },
      hasLogin () {
        return this.$store.getters.hasLogin
      }
    },
    methods: {
      getTopics: function (n, s) {
        this.$axios.get('/topics_latest/' + n + '-' + s + '.json')
          .then(response => {
            this.tempTopics = response.data
            if (this.tempTopics.length === 0) {
              this.limit = 'No More Topics'
              return this.limit
            }
            this.tempTopics.forEach(topic => {
              this.$axios.get('/topic/' + topic.id + '/news_latest/1.json')
                .then(response => {
                  Vue.set(topic, 'news_title', response.data[0].news_title)
                  Vue.set(topic, 'news_date', response.data[0].news_date.slice(0, 10))
                  Vue.set(topic, 'news_url', response.data[0].news_url)
                  Vue.set(topic, 'image_url',
                    (response.data[0].image_url.length === 0 ? 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg' : response.data[0].image_url))
                  this.topics.push(topic)
                })
            })
            console.log(this.topics)
          })
          .catch(e => {
            this.errors.push(e)
            console.log(this.errors)
          })
      },
      loadMore: function () {
        this.busy = true;
        this.counter += 12
        this.getTopics(12, this.counter)
        this.busy = false;
      },
      checkSubscribe: function (id) {
        return this.collection.includes(id)
      },
      hasSubscribe (id){
        return this.collection.includes(id)
      },
      subscribe (id) {
        this.$axios.put('users/update/' + this.user['id'] + '/', {
          first_name: this.user['first_name'],
          last_name: this.user['last_name'],
          collection_topic_id_array: this.collection.concat([id]).toString()
        })
          .then(response => {
            console.log(response.data)
            this.collection = this.collection.concat([id])
            this.$store.commit('update', response.data)
          })
      },
      unsubscribe (id) {
        this.$axios.put('users/update/' + this.user['id'] + '/', {
          first_name: this.user['first_name'],
          last_name: this.user['last_name'],
          collection_topic_id_array: this.collection.filter(item => item !== id).toString()
        })
          .then(response => {
            console.log(response.data)
            this.collection = this.collection.filter(item => item !== id)
            this.$store.commit('update', response.data)
          })
      }
    },
    created: function () {
      console.log(this.counter)
      this.getTopics(12, 0)
      if (this.user !== null) {
        if (this.user['collection_topic_id_array']) {
          this.collection = this.user['collection_topic_id_array'].split(',').map(Number)
        } else {
          this.collection = []
        }
      }
    },
    directives: {infiniteScroll}

  }
</script>

<style scoped>

  .col-md {
    margin: 20px auto 20px;
  }

  .glyphicon-link {
    text-decoration: none;
    color: green;
    display: inline-block;
  }

  .bt a {
    text-decoration: none;
    color: white;
    display: block;
    cursor: pointer;
  }

  .container {
    border-radius: 5px;
    padding: 1px;
    margin: 5px auto;
    width: 90%;
    background-color: transparent;
  }

  .card {
    width: 25rem;
    margin: 0 auto;
    display: block;
  }

  .card-block p {
    margin-left: 10px;
    color: black;
    font-family: "Helvetica Neue Light";
    font-size: 18px;
  }

  .card-block .glyphicon-heart, .glyphicon-heart-empty {
    color: #DC143C;
    background-color: transparent;
    text-decoration: none;
  }

  .card-block h4 {
    margin-left: 5px;
    font-size: 30px;
    font-weight: bold;
    font-family: "SansSerif";
  }

  img {
    width: auto;
    height: auto;
    max-height: 100%;
    max-width: 100%;
  }

  .row {
    display: flex;
    flex-wrap: wrap;
    flex-flow: row wrap;
  }

  .card:hover {
    box-shadow: 2rem 0 2rem grey;
  }

  .bt {
    background: linear-gradient(to bottom, darkgrey, black);
    width: auto;
    margin: auto;
    height: 20px;
    text-align: center;
  }

  .bt > a:hover {
    background-color: grey;
    color: black;
  }

  span {
    padding-left: 10%;
  }

  small {
    float: right;
    padding-right: 10%;
  }
</style>
