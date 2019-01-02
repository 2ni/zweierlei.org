<template>
  <div class="container">
    <Loading v-if="isLoading" />

    <NotFound v-else-if="notFound" />

    <template v-else>
    
      <div class="tile is-ancestor">
        <div class="tile is-parent">
          <div class="tile is-child notification is-warning is-paddingless card">
            <div class="card-header">
              <p class="card-header-title">Your account</p>
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
                    <p v-show="errors.has(element)" class="help is-danger">{{ errors.first(element) }}</p>
                  </div>
                </template>

                <div class="field">
                  <div class="control">
                    <button class="button is-link" :disabled="isSaving">
                      <span v-if="isSaving" class="icon is-small"><i class="fas fa-sync-alt fa-spin"></i></span>
                      <span>{{ $t('save') }}</span>
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
  mounted() {
    userService.get()
      .then((responseUser) => {
        this.user = responseUser.data;
        this.isLoading = false;
      })
      .catch((errorUser) => {
        this.notFound = true;
        this.isLoading = false;
      });
  },
  data() {
    return {
      user: [],
      elements: ['firstname', 'lastname', 'email', 'password'],
      isLoading: true,
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
      userService.save(this.user)
        .then((responseSaving) => {
          this.isSaving = false;
          this.$store.state.alert = { message: this.$t('data.saved'), type: 'success' };
        })
        .catch((errorSaving) => {
          this.isSaving = false;
          const { response: { status }, response: { data: { msg } } } = errorSaving;
          if (status === 422) {
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
            this.$store.state.alert = { message: this.$t('data.error', { msg: JSON.stringify(msg) }), type: 'danger' };
          }
        });
    },
  },
  components: {
    Loading,
    NotFound,
  },
};
</script>
