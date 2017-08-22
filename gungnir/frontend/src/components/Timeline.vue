<template>
  <div id="timeline">
    <div id="timeline_topic">
      <span class="topic-name">Topic: {{topic.topic_name}}</span>
      <span v-if="hasLogin">
        <a class="glyphicon glyphicon-heart-empty btn btn-info " @click="subscribe" v-if="!hasSubscribed"></a>
        <a class="glyphicon glyphicon-heart btn btn-info" @click="unsubscribe" v-if="hasSubscribed"></a>
      </span>
      <a id="line-chart-button" type="button" class="btn btn-info fa " data-toggle="modal" data-target="#myModal">
        <i class="fa">&#xf080;</i>
      </a>
      <div class="modal fade" id="myModal" role="dialog">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-body">
              <schart canvasId="myCanvas" type="line" width=500  height=400  :data="data" :options="options">
              </schart>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="visualization" ref="visualization" :style="{height:v_height}"></div>
  </div>
</template>

<script type="text/javascript">
  import Schart from 'vue-schart'
  export default {
    data () {
      return {
        v_height: (screen.height - 180) + 'px',
        topicId: this.$route.params.topicId,
        topic: '',
        collection: [],
        news: {},
        errors: [],
        isLoading: false,
        data: [],
        options: {
          title: "Popularity in the past week",
          fillColor: '#000000'
        }
      }
    },
    computed: {
      user () {
        return this.$store.getters.user
      },
      hasLogin () {
        return this.$store.getters.hasLogin
      },
      hasSubscribed () {
        return this.collection.includes(this.topicId)
      }
    },
    created: function () {
      this.$axios.get('/topic/' + this.topicId + '.json')
        .then(response => {
          this.topic = response.data
          console.log(this.topic)
        })
      this.$axios.get('/topic/' + this.topicId + '/news.json')
        .then(response => {
          this.news = response.data
          this.isLoading = true
        })
        .catch(e => {
          this.errors.push(e)
          console.log(this.errors)
        })
      this.$axios.get('topic/count/' + this.topicId + '.json')
        .then(response => {
          response.data.forEach(item => {
            this.data.push({
              name: item.news_date.slice(5),
              value: item.news_counter
            })
          })
        })
      if (this.user !== null) {
        if (this.user['collection_topic_id_array']) {
          this.collection = this.user['collection_topic_id_array'].split(',').map(Number)
        } else {
          this.collection = []
        }
      }
    },
    watch: {
      isLoading: function () {
        if (this.isLoading) {
          var timelineObjs = []
          console.log(this.news)
          this.news.forEach(function (obj) {
            timelineObjs.push({
              'media': {'url': obj.image_url},
              'start_date': {
                'month': obj.news_date.slice(5, 7),
                'day': obj.news_date.slice(8, 10),
                'year': obj.news_date.slice(0, 4)
              },
              'text': {
                'headline': obj.news_title,
                'text': obj.news_summarize + `<div><a href=${obj.news_url}>source</a></div>`
              }
            })
          })
          var option = {}
          new TL.Timeline(this.$refs.visualization, {'events': timelineObjs}, option)
        }
      }
    },
    methods: {
      subscribe () {
        this.$axios.put('users/update/' + this.user['id'] + '/', {
          first_name: this.user['first_name'],
          last_name: this.user['last_name'],
          collection_topic_id_array: this.collection.concat([this.topicId]).toString()
        })
          .then(response => {
            console.log(response.data)
            this.collection = this.collection.concat([this.topicId])
            this.$store.commit('update', response.data)
          })
      },
      unsubscribe () {
        this.$axios.put('users/update/' + this.user['id'] + '/', {
          first_name: this.user['first_name'],
          last_name: this.user['last_name'],
          collection_topic_id_array: this.collection.filter(item => item !== this.topicId).toString()
        })
          .then(response => {
            console.log(response.data)
            this.collection = this.collection.filter(item => item !== this.topicId)
            this.$store.commit('update', response.data)
          })
      }
    },
    components: {
      Schart
    }
  }
</script>

<style scoped>
  #line-chart-button {
    color: darkgreen;
  }

  #timeline_topic {
    height: 10%;
    padding-left: 5%;
    font-family: "Sans-Serif";
    /*font-style: italic;*/
    color: black;
    font-weight: bold;
    font-variant: normal;
    background: linear-gradient(to right, lightgrey, transparent);
    font-size: 150%;
    margin-top: 2%;
  }

  #timeline_topic span {
    display: inline-block;
  }

  .btn {
    line-height: 50%;
    margin: auto;
  }

  .btn-info {
    border-color: transparent;
    /*color: darkgreen;*/
    background-color: transparent;
    margin-left: 10px;
    font-size: 20px;
  }

  .modal-header button {
    color: white;
    size: 30px;
  }

  .modal-footer {
    background-image: linear-gradient(to top left, lightgray, black);
    color: white;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: medium;
    font-style: inherit;
  }

  /*#timeline_topic span a*/
  /*{*/
  /*display: inline-block;*/
  /*margin-left: 10px;*/
  /*color: #c9302c;*/
  /*text-decoration: inherit;*/
  /*}*/
  .glyphicon {
    color: red;
    text-decoration: none;
  }

  /*a*/
  /*{*/
  /*text-decoration: none;*/
  /*color: #c9302c;*/
  /*display: inline-block;*/
  /*margin-left: 10px;*/
  /*}*/

</style>
