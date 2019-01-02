const user = {
  computed: {
    $user() {
      const userString = localStorage.getItem('user');
      return userString ? JSON.parse(userString) : null;
    },
  },
};

export { user };
