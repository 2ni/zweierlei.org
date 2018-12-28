const localize = {
  methods: {
    $localize(value, lang=null) {
      return '/' + (lang ? lang : this.$i18n.locale) + (value.charAt(0) === '/' ? '' : '/') + value;
    },
  },
};

export { localize };
