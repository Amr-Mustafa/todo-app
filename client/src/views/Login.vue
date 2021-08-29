<template>
  <b-container>
    <b-row>
      <b-col sm="3" align-self="center">
        <h1>Login</h1>
        <b-form @submit.prevent="submit">
          <b-form-group
            id="input-group-1"
            label="Email address:"
            label-for="input-1"
          >
            <b-form-input
              id="input-1"
              v-model="form.email"
              type="email"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="input-group-2"
            label="Password:"
            label-for="input-2"
          >
            <b-form-input
              id="input-2"
              v-model="form.password"
              type="password"
              required
            ></b-form-input>
          </b-form-group>

          <b-button variant="success" type="submit">Login!!</b-button>
          <p v-if="showError">Incorrect user credentials!</p>
        </b-form>
        <b-button @click="githubLogin">
          <b-icon icon="github"></b-icon>
          Login With Github
        </b-button>
      </b-col>
    </b-row>
  </b-container> 
</template>

<script>

import { mapActions, mapMutations } from "vuex";
import axios from "axios";
import Vue from 'vue'


var source = new EventSource("http://localhost:8000/stream");

export default {
  mounted() {
    source.addEventListener('auth', this.auth);
  },
  name: "Login",
  components: {},
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
    };
  },
  methods: {
    ...mapActions(["LogIn"]),
    ...mapMutations(["setUser"]),
    async submit() {
      const User = new FormData();
      User.append("email", this.form.email);
      User.append("password", this.form.password);
      try {
          await this.LogIn(User);
          this.$router.push("/items");
          this.showError = false
      } catch (error) {
        this.showError = true
      }
    },
    async githubLogin() {
      fetch(`https://github.com/login/oauth/authorize?
        response_type=token
        &client_id=cb72d955c84365f9f932
        &redirect_uri=http://localhost:8000/api/login/github
        &state=NkYYkZL1uafLZToPgkINnDU3U9euVz`)
      .then(response => window.open(response.url));
    },
    auth(event) {
      var data = JSON.parse(event.data);
      console.log(data);
      Vue.set(this.$store.state, 'user', {
        "email": data.email,
        "jwt_token": data.jwt
      });
    }
  },
};
</script>
