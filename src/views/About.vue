<template>
  <article id="about">
    <header>
      <h1>About me...</h1>
    </header>
    <div>
    {{ $t('hello') }}
    </div>
  </article>
</template>

<style>
#about {
  height: 100%;
  width: 100%;
  margin: 0;
  display: table;
  border: 3px solid blue;
}

#about header {
  display: table-row;
  background: lightgreen;
}

#about div {
  background: green;
  display: table-cell;
  padding-top: 1em;
  height: 100%;
}

</style>
