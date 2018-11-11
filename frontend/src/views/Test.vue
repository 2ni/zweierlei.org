<template>
<main id="main-test">
    <header>
      <div>
        <p class="title">Full height page layout</p>
        <p class="subtitle">I have some height</p>
      </div>
    </header>
    <div>
      <div class="content">
        <p>I take up the remaining height</p>
      </div>
    </div>
</main>
</template>

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
