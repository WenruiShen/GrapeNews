<template>
  <div>
    <footer class="footer">
      <div class="container">
        <router-link to="/about"><a>About Us</a></router-link>
        &nbsp;
        <router-link to="/test">Copy Right</router-link>
      </div>
    </footer>
  </div>
</template>

<style scoped>
  .footer {
    text-align: center;
    width: inherit;
    background-color: black;
    height: 40px;
    position: relative;
    line-height: 40px;
  }

  a {
    color: grey;
    text-decoration: none;
    font-family: "Harlow Solid Italic";
  }

  a:hover {
    color: lightgrey;
    text-decoration: none;
    font-family: "Bodoni MT";
  }

</style>
