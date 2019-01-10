<template>
  <div class="container">
    <Loading v-if="isLoading" />

    <NotFound v-else-if="notFound" />

    <template v-else>

      <div class="tile is-ancestor">
        <div class="tile is-parent">
          <div class="tile is-child notification is-warning is-paddingless card">
            <div class="card-header">
              <p class="card-header-title">{{ isProfile ? 'Your account' : 'Registration' }}</p>
            </div>
            <div class="card-content">

              <form @submit.prevent="processSubmit">

                <template v-for="element in elements">
                  <div class="field">
                    <label class="label">{{ $t('user.'+element) }}</label>
                    <p class="control has-icons-left has-icons-right">
                    <input
                       v-validate="'required|max:100'"
                       :name="element"
                       class="input"
                       :type="typeOfElement(element)"
                       :placeholder="$t('user.help.'+element)"
                       v-model="user[element]"
                     >
                     <span class="icon is-small is-left">
                       <i class="fas fa-coffee"></i>
                     </span>
                     <span v-show="errors.has(element)" class="icon is-small is-right">
                       <i class="fas fa-times has-text-danger"></i>
                     </span>
                    </p>
                    <!-- <p v-show="errors.has(element)" class="help is-danger">{{ errors.first(element) }}</p> -->
                    <div v-show="errors.has(element)" class="is-small">
                      <p class="help is-danger" v-for="error in errors.collect(element)">{{ error }}</p>
                    </div>
                  </div>
                </template>

                <div class="field">
                  <div class="control">
                    <button class="button is-link" :disabled="isSaving||errors.all().length > 0">
                      <span v-if="isSaving" class="icon is-small"><i class="fas fa-sync-alt fa-spin"></i></span>
                      <span>{{ $t(isProfile ? 'user.save' : 'user.create') }}</span>
                    </button>
                  </div>
                </div>

              </form>


            </div>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script type="ts">
import { userService } from '@/services';
import Loading from '@/components/Loading.vue';
import NotFound from '@/components/NotFound.vue';

export default {
  props: [ 'type' ],
  beforeMount() {
    if (this.isProfile) {
      userService.get()
        .then((responseUser) => {
          this.user = responseUser;
          this.isLoading = false;
        })
        .catch((errorUser) => {
          this.notFound = true;
          this.isLoading = false;
        });
    }
  },
  data() {
    return {
      user: {},
      elements: ['firstname', 'lastname', 'email', 'password'],
      isLoading: this.isProfile ? true : false,
      isSaving: false,
      notFound: false,
    };
  },
  methods: {
    typeOfElement(element) {
      return (element === 'password' ? 'password' : 'text');
    },
    processSubmit(e) {
      this.isSaving = true;
      const entrypoint = this.isProfile ? 'users' : 'register';

      // keep old pw (do not update) if not given
      if (this.isProfile && !this.user.password) {
        delete this.user.password;
      }

      this.$store.dispatch('authentication/save', { entrypoint, user: this.user })
        .then((responseSaving) => {
          this.isSaving = false;
          this.$store.dispatch('alert/success', this.$t('data.saved'));
          if (!this.isProfile) {
            this.$router.push({name: 'Profile'});
          }
        })
        .catch((errorSaving) => {
          this.isSaving = false;
          const { response: { status }, response: { data: { msg } } } = errorSaving;
          if ([422, 409].includes(status)) {
	    // set errors returned from backend
	    // https://github.com/baianat/vee-validate/issues/1153
	    for (const element in msg) {
	      if (msg.hasOwnProperty(element)) {
		const field = this.$validator.fields.find({name: element});
		field.setFlags({invalid: true});
		this.errors.add({
		  field: field.name,
		  msg: msg[element],
		  id: field.id,
		  scope: field.scope,
		});
	      }
	    }
          } else {
            this.$store.dispatch('alert/error', JSON.stringify(msg));
          }
        });
    },
  },
  computed: {
    isProfile() {
      return this.type === 'profile';
    },
  },
  components: {
    Loading,
    NotFound,
  },
};
</script>
