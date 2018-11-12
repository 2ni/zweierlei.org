<template>
  <div class="container">
    <div class="box">
      <h3 class="title">Login</h3>
      <form @submit.prevent="handleSubmit">
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" :class="{'is-danger': submitted && !username}" type="email" v-model="username" placeholder="Email">
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <!--
            <span class="icon is-small is-right">
              <i class="fas fa-check"></i>
            </span>
            -->
            <span class="icon is-small is-right" v-show="submitted && !username">
              <i class="fas fa-times has-text-danger"></i>
            </span>
            <p v-show="submitted && !username" class="help is-danger">Email is required</p>
          </p>
        </div>
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" :class="{'is-danger': submitted && !password}" type="password" v-model="password" placeholder="Password">
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
            <span class="icon is-small is-right" v-show="submitted && !password">
              <i class="fas fa-times has-text-danger"></i>
            </span>
            <p v-show="submitted && !password" class="help is-danger">Password is required</p>
          </p>
        </div>
        <div class="field">
          <p class="control">
            <button class="button is-link" :class="{'is-loading': loggingIn}" :disabled="loggingIn">Login</button>
          </p>
          <p v-show="loginFailMessage" class="help is-danger">{{ loginFailMessage }}</p>
        </div>
      </form>
    </div>
  </div>
</template>

<script type="ts">
export default {
  data() {
    return {
      username: '',
      password: '',
      submitted: false,
      loginFailMessage: null,
    };
  },
  created() {
    this.$store.dispatch('authentication/logout');
  },
  computed: {
    loggingIn() {
      return this.$store.state.authentication.status === 'loggingIn';
    },
  },
  methods: {
    handleSubmit(e) {
      this.submitted = true;
      const { username, password } = this;
      const { dispatch } = this.$store;
      if (username && password) {
        dispatch('authentication/login', { username, password }).then(
          (user) => {
            const f = this.$route.query.f;
            this.$router.push(f ? f : '/' + this.$route.params.locale);
          },
          (error) => {
            this.loginFailMessage = error;
          },
        );
      }
    },
  },
};
</script>

<style scoped>
.container {
  padding: 1em 0;
}
</style>
