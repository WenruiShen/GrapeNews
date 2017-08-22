<template>
  <div class="search">
    <div class="container fuiled ">
      <div class="input-group">
        <input list="topic" name="topic" type="text" class="form-control" placeholder="Search for..." v-model="value">
        <datalist id="topic">
          <option v-for="topic in hints"> {{ topic.topic_name }}</option>
        </datalist>
        <div class="input-group-btn">
          <button class="btn btn-default" type="button" @click="searchValue">Search</button>
          <router-link to="/topic/list">
            <button type="button" class="btn btn-default">Show All Topics</button>
          </router-link>
        </div>
      </div>
      <hr/>
      <div class="result">
        <div>
          <ul>
            <li v-for="(topic, index) in results">
              <router-link :to="{ name: 'Timeline' , params: { topicId: topic.id }}">
                <p>{{ topic.topic_name }}</p>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import _ from 'lodash'
  export default {
    data () {
      return {
        value: '',
        hints: [],
        results: [],
        errors: []
      }
    },
    watch: {
      value: function () {
        if (this.value.length > 2) {
          this.lookupValue()
        }
      }
    },
    methods: {
      lookupValue: _.debounce(function () {
        var app = this
        this.$axios.get('/topic/search/' + app.value)
          .then(response => {
            if (response.data.length === 0) {
              app.hints = [{topic_name: 'No relevant topic'}]
            } else {
              app.hints = response.data
            }
          })
          .catch(e => {
            app.errors.push(e)
            console.log(app.errors)
          })
      }, 500),
      searchValue: function () {
        this.$axios.get('/topic/search/' + this.value)
          .then(response => {
            this.results = response.data
          })
          .catch(e => {
            this.errors.push(e)
            console.log(this.errors)
          })
      }
    }
  }
</script>

<style scoped>
  .search {
    padding: 50px 50px;
    background: linear-gradient(to bottom, rgba(100, 100, 100, 0.2) 0%, rgba(255, 255, 255, 0.5) 40%, #ffffff 100%);
  }

  .input-group button {
    /*display: inline-block;*/
    background-color: black;
    color: white;
    text-decoration: none;
    border-top: none;
    border-bottom: none;
    border-left: none;
    height: 34px;
    border-radius: 0px;
    border-color: white;
  }

  .input-group button:hover {
    background-color: silver;
    color: black;
  }

  .result {
    background-color: whitesmoke;
    padding: 20px;
  }

  .result li, p {
    list-style-type: decimal;
    /*display: block;*/
    font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
    color: black;
    font-size: medium;
    font-weight: 200;
  }

  .result li:hover {
    background-color: lightsteelblue;
  }

  a {
    text-decoration: none;
    /*color: black;*/
    font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
  }

</style>
