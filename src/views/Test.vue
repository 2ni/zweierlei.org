<template>
<main id="main-test">
    <header>
      <div>
        <p>test</p>I have some height
      </div>
    </header>
    <div>
      <div class="content">
        I take up the remaining height
          <md-card>
            <md-card-header>
              <div class="md-title">Foo</div>
              <div class="md-subhead">by ddm</div>
            </md-card-header>
            <md-card-content>
              <md-button v-on:click="fillTable" class="md-raised md-primary">Fill it up!</md-button>
              <md-button v-on:click="clearTable" class="md-raised md-primary">Clear data!</md-button>
              <md-table>
                <md-table-row>
                  <md-table-head>First name</md-table-head>
                  <md-table-head>Last name</md-table-head>
                  <md-table-head>Email</md-table-head>
                </md-table-row>
                <md-table-row v-for="contact in contacts" :key="contact.email">
                  <md-table-cell>{{contact.firstname}}</md-table-cell>
                  <md-table-cell>{{contact.lastname}}</md-table-cell>
                  <md-table-cell>{{contact.email}}</md-table-cell>
                </md-table-row>
              </md-table>
            </md-card-content>
          </md-card>
      </div>
    </div>
</main>
</template>

<script type="ts">
export default {
  data() {
    return {
      contacts: [{firstname: 'John', lastname: 'Doe', email: 'john.doe@gmail.com'}],
    };
  },
  methods: {
    fillTable() {
      this.contacts.push({firstname: 'Foo', lastname: 'Bar', email: 'foobar@mail.com'});
    },
    clearTable() {
      this.contacts.splice(0, this.contacts.length);
    },
  },
};
</script>

<style>
#main-test {
    height: 100%;
    width: 100%;
    margin: 0;
    display: table;
}

#main-test header {
    height: 0%;
    background-color: grey;
    display: table-row;
}

#main-test header div {
  display: table-cell;
  padding: 10px;
}

#main-test > div {
    background-color: pink;
    display: table-row;
}

#main-test .content {
  display: table-cell;
  padding: 10px;
}

</style>
