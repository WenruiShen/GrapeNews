<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <table class="table table-striped table-hover">
          <thead>
          <tr>
            <th>Number</th>
            <th>Topics</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(topic, index) in list">
            <td id="1">{{index + 1}}</td>
            <td>
              <router-link :to="{ name: 'Timeline' , params: { topicId: topic.id }}">
                {{ topic.topic_name }}
              </router-link>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  export default{
    data () {
      return {
        list: [],
        errors: []
      }
    },
    created: function () {
      this.$axios.get('/topic.json')
        .then(response => {
          this.list = response.data
        })
        .catch(e => {
          this.errors.push(e)
          console.log(this.errors)
        })
    },
  }

</script>

<style scoped>
  .container {
    width: auto;
    margin-left: 3%;
    margin-right: 3%;
    margin-top: 3%;
  }

  tbody a {
    color: black;
    text-decoration: none;
  }

  * {
    font-family: "Helvetica Neue Light", "HelveticaNeue-Light", "Helvetica Neue", Calibri, Helvetica, Arial, sans-serif;
    font-size: medium;
    font-style: oblique;
  }


</style>
