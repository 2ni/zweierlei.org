<template>
  <div class="container">
    <h1 class="title">About me...</h1>
    <p>{{ $t('hello') }}</p>
    <p>{{ $route.params }}</p>
    <p>{{ $route.fullPath }}</p>
  </div>
</template>
