<template>
  <div class="sign">
    <div class="container">
      <div class="row">
        <p class="form-tittle">
          Sign Up
        </p>
        <form class="login">
          <input type="text" placeholder="Username" v-model="username">
          <input type="text" placeholder="E-mail" v-model="email">
          <input type="password" placeholder="Password" v-model="password">
          <input type="submit" value="Sign Up" class="btn btn-default" @click.prevent="signup">
          <div class="append">
            <div class="row">
              <div class="col-md-6">
                <div class="text">
                  <label>
                    Already have an account?
                  </label>
                </div>
              </div>
              <div class="col-md-6 finish">
                <a class="btn btn-default" @click="login">Login</a>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
  export default {
    data () {
      return {
        username: '',
        email: '',
        password: ''
      }
    },
    methods: {
      login () {
        this.$router.push({path: '/login'})
      },
      signup () {
        this.$axios.post('users/register/', {
          username: this.username,
          email: this.email,
          password: this.password
        })
          .then(response => {
            console.log(response.data)
            this.$store.commit('signup', response.data)
            this.$router.push({path: '/'})
          })
          .catch(function (error) {
            console.log(error)
          })
      },
    }
  }
</script>

<style scoped>

  .sign {
    background: linear-gradient(to bottom, rgba(100, 100, 100, 0.2) 0%, rgba(255, 255, 255, 0.5) 40%, #ffffff 100%);;
  }

  p.form-tittle {
    font-family: 'Open Sans', sans-serif;
    font-size: 30px;
    font-weight: 600;
    text-align: center;
    color: black;
    margin-top: 8%;
    text-transform: uppercase;
    letter-spacing: 4px;
  }

  form
  {
    width: 25%;
    margin: 0 auto;
    font-size: 60px;
  }

  form.login input[type="text"], form.login input[type="password"] {
    width: 100%;
    margin: 0;
    padding: 5px 10px;
    background: 0;
    border: 0;
    border-bottom: 1px solid black;
    outline: 0;
    font-style: italic;
    font-size: 20px;
    font-weight: 400;
    letter-spacing: 1px;
    margin-bottom: 5px;
    color: black;
  }

  form.login input[type="submit"] {
    width: 100%;
    font-size: 20px;
    text-transform: uppercase;
    font-weight: 500;
    margin-top: 16px;
    outline: 0;
    cursor: pointer;
    letter-spacing: 1px;
  }

  form.login input[type="submit"]:hover {
    transition: background-color 0.5s ease;
  }

  form.login .remember-forgot {
    float: left;
    width: 100%;
    margin: 10px 0 0 0;
  }

  form.login .finish {
    min-height: 20px;
    margin-top: 10px;
    margin-bottom: 10px;
  }

  form.login label, form.login a {
    font-size: 20px;
    font-weight: 400;
    color: black;
  }

  form.login a {
    transition: color 0.5s ease;
  }

  form.login a:hover {
    transition: background-color 0.5s ease;
  }


</style>
