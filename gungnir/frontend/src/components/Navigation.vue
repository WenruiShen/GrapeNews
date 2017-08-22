<template>
  <nav class="navbar navbar-inverse">
    <div class="container-fluid">
      <!-- Brand and toggle get grouped for better mobile display -->
      <div class="navbar-header">
        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                data-target="#nav" aria-expanded="false">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="#">Grape News</a>
      </div>

      <!-- Collect the nav links, forms, and other content for toggling -->
      <div class="collapse navbar-collapse" id="nav">
        <ul class="nav navbar-nav">
          <li><a href="#">Home</a></li>
          <li>
            <router-link to="/about">About</router-link>
          </li>
          <li>
            <router-link to="/search">Search</router-link>
          </li>
          <li>
            <router-link to="/topic/list">Topics</router-link>
          </li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
          <li>
            <router-link to="/login" v-if="!hasLogin" @click="login">
              <span class="glyphicon glyphicon-log-in"></span>
              &nbsp; Login
            </router-link>
          </li>
          <li>
            <router-link to="/signup" v-if="!hasLogin" @click="signup"><span class="glyphicon glyphicon-user"></span>&nbsp;
             Signup
            </router-link>
          </li>
          <li class="dropdown" v-if="hasLogin">
            <router-link id="2" :to="{ name: 'User' , params: { user: username }}" @click="mySetting"><span
              class="glyphicon glyphicon-log-out"></span>&nbsp;{{ username }}
            </router-link>
            <a href="#" class="dropdown-toggle " data-toggle="dropdown" role="button"
               aria-haspopup="true" aria-expanded="false" v-if="notify != null">
            <span class="glyphicon glyphicon-info-sign">
              <sup>{{ notify.length }}</sup>
            </span>
            </a>
            <ul class="dropdown-menu">
              <li v-for="item in notify">
                <router-link :to="{ name: 'Timeline' , params: { topicId: item.id }}">{{ item.topic_name }}
                </router-link>
              </li>
            </ul>
          </li>
        </ul>
      </div><!-- /.navbar-collapse -->
    </div><!-- /.container-fluid -->
  </nav>


</template>


<script>
  import {mapGetters} from 'vuex'
  export default {
    data () {
      return {
        data: '',
        updates: [],
        updatesObj: []
      }
    },
    computed: {
      user () {
        return this.$store.getters.user
      },
      username () {
        return this.$store.getters.username
      },
      hasLogin () {
        return this.$store.getters.hasLogin
      },
      collection () {
        if (this.$store.getters.userSubscribeTopic == null) {
          return []
        }
        return this.$store.getters.userSubscribeTopic.split(',').map(Number)
      },
      notify () {
        if (this.updates.length === 0 || this.collection.length === 0) {
          return null
        }
        var setUpdates = new Set(this.updates)
        var setCollection = new Set(this.collection)
        var setNotify = new Set([...setUpdates].filter(x => setCollection.has(x)))
        console.log(setNotify)
        var notifyArr = Array.from(setNotify)
        if (notifyArr.length === 0) {
          return null
        }
        var notifyObjs = this.updatesObj.filter(function (el) {
          return setNotify.has(el.id);
        })
        return notifyObjs
      }
    },
    methods: {
      search () {
        this.$router.push({path: '/search'})
      },
      login () {
        this.$router.push({path: '/login'})
      },
      signup () {
        this.$router.push({path: '/signup'})
      },
      topic () {
        this.$router.push({path: '/topic/list'})
      },
      mySetting () {
        this.$router.push({path: '/settings/' + this.username})
      }
    },
    created: function () {
      this.$axios.get('/topic/update.json')
        .then(response => {
          var tempArr = []
          var tempArrObj = []
          if (response.data !== null) {
            response.data.forEach(function (obj) {
              tempArr.push(obj.id)
              tempArrObj.push(obj)
            })
//            console.log(this.tempArr)
            this.updates = tempArr
            this.updatesObj = tempArrObj
            console.log(this.updates)
            console.log(this.updatesObj)
          }
        })
    }
  }
</script>

<style scoped>

  .navbar {
    margin-bottom: 0px;
    min-height: 60px;
    font-family: 'Yanone Kaffeesatz', sans-serif;
  }

  .navbar-brand {

  }

  .container-fluid {
    /*height: 60px;*/
  }

  .navbar-header {
    height: 100%;
  }

  .navbar-brand {
    height: 100%;
    font-size: 35px;
    letter-spacing: 3px;
    color: white;
    display: block;
    margin-left: 20px;
    padding-left: 30px;
    padding-top: 20px;
    padding-bottom: 20px;
  }

  .nav li a {
    padding-top: 20px;
    padding-bottom: 20px;
    display:inline-block;
  }

  .navbar-nav {
    margin-left: 3%;
  }

  .nav li {
    margin-left: 5px;
    margin-right: 5px;
    font-size: 20px;
  }
</style>
