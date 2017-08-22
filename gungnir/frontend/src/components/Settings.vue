<template>
  <div id="Usersetting">
    <h1>User Profiles</h1>
    <div v-if="!hasLogin">
      <p style="padding: 50px;"> You have been logged out</p>
    </div>
    <div v-if="hasLogin" class="fluid container">
      <form id="1">
        <form class="form-horizontal">
          <div class="form-group">
            <label for="uname" class="col-sm-2 control-label">User Name:</label>
            <div class="col-sm-3">
              <input type="text" class="form-control" id="uname" readonly="readonly" :value="user['username']">
            </div>
          </div>
          <div class="form-group">
            <label for="lname" class="col-sm-2  control-label">E-mail:</label>
            <div class="col-sm-3">
              <input type="text" id="email" class="form-control" readonly="readonly" :value="user['email']">
            </div>
          </div>
          <div class="form-group">
            <label for="fname" class="col-sm-2 control-label">First Name:</label>
            <div class="col-sm-3">
              <input type="text" class="form-control" id="fname" placeholder="first name" v-model="f_name">
            </div>
          </div>
          <div class="form-group">
            <label for="lname" class="col-sm-2 control-label">Last Name:</label>
            <div class="col-sm-3">
              <input type="text" class="form-control" id="lname" placeholder="last name" v-model="l_name">
            </div>
          </div>
          <div class="form-group">
            <label for="ctime" class="col-sm-2  control-label">Joined Date:</label>
            <div class="col-sm-3">
              <input type="text" id="ctime" class="form-control" readonly="readonly"
                     :value="user['date_joined'].slice(0,10)">
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-2  control-label">Subscribe topics:</label>
            <div class="col-sm-10">
              <div id="box">
                <table style="width:100%">
                  <tr v-for="topic in topics_collection">
                    <td><a @click="view(topic.id)">{{ topic.topic_name}}</a></td>
                    <td>
                      <button @click="unsubscribe(topic.id)">unsubscribe</button>
                    </td>
                  </tr>
                </table>
              </div>
            </div>
          </div>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10 submit">
              <button type="submit" class="btn btn-default" @click="update">Submit</button>
              <button class="btn btn-default" @click="logout">Logout</button>
            </div>
          </div>
        </form>
      </form>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default{
    data () {
      return {
        user_data: [],
        f_name: '',
        l_name: '',
        collection: [],
        topics_collection: []
      }
    },
    computed: mapGetters([
      'user',
      'hasLogin'
    ]),
    methods: {
      logout () {
        this.$store.commit('logout')
        this.$router.push({path: '/'})
      },
      update () {
        this.$axios.put('users/update/' + this.user['id'] + '/', {
          first_name: this.f_name,
          last_name: this.l_name,
          collection_topic_id_array: this.collection.toString()
        })
          .then(response => {
            console.log(response)
            this.$store.commit('update', response.data)
          })
      },
      unsubscribe (topic) {
        this.collection = this.collection.filter(item => item !== topic)
        this.topics_collection = this.topics_collection.filter(item => item.id !== topic)
      },
      view (topicId) {
        this.$router.push({name: 'Timeline', params: {topicId: topicId}})
      }
    },
    created: function () {
      this.f_name = this.user['first_name']
      this.l_name = this.user['last_name']
      this.collection = this.user['collection_topic_id_array'].split(',').map(Number)
      this.collection.forEach(topic => {
        this.$axios.get('/topic/' + topic + '.json')
          .then(response => {
            this.topics_collection.push(response.data)
          })
      })
    }
  }
</script>

<style scoped>
  #box {
    width: 500px;
    border: 3px solid dimgray;
    padding: 25px;
  }

  h1 {
    display: inline-block;
    margin-left: 3%;
    font-style: italic;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  }

  .btn {
    margin-top: 10%;
    margin-bottom: 5%;
    color: white;
    background-color: black;
  }

  #Usersetting {

    background: linear-gradient(to bottom, rgba(100, 100, 100, 0.2) 0%, rgba(255, 255, 255, 0.5) 40%, #ffffff 100%);;
  }

  input {
    border: none;
    background-color: transparent;
    border-bottom: 1px lightslategray solid;
    outline: none;
  }

  .col-sm-3 span {
    display: inline-block;
    text-align: center;
    margin-top: 5%
  }
</style>
