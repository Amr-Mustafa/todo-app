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

          <b-button variant="success" type="submit">Login</b-button>
        </b-form>
      </b-col>
    </b-row>
  </b-container> 
</template>

<script>
import { mapActions } from "vuex";
export default {
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
  },
};
</script>
