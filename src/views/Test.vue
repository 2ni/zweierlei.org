<template>
<main id="test">
    <header>
        <p>test</p>I have some height
    </header>
    <div>
        I take up the remaining height
    </div>
</main>
</template>

<style>
#test {
    height: 100%;
    width: 100%;
    margin: 0;
    display: table;
}

#test header {
    height: 0%;
    background-color: grey;
    display: table-row;
}

#test div {
    background-color: pink;
    display: table-row;
}

</style>
