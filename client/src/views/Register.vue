<template>
  <b-container>
    <b-row>
      <b-col sm="3" align-self="center">
        <h1>Register</h1>
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

          <b-button variant="success" type="submit">Register</b-button>
        </b-form>
      </b-col>
    </b-row>
  </b-container> 
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Register",
  components: {},
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      showError: false
    };
  },
  methods: {
    ...mapActions(["Register"]),
    async submit() {
      try {
        await this.Register(this.form);
        this.$router.push("/items");
        this.showError = false
      } catch (error) {
        console.log(error);
        this.showError = true
      }
    },
  },
};
</script>
