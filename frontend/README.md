## Debug
access vue via developer console:
- click on Root in Vue extension 1st

```
$vm.<variable>
```

## Useful stuff
```
for i in {1..10}; do convert -size `python -c "import random; print random.randint(500,1000)"`x`python -c "import random; print random.randint(500,1000)"` xc:`python -c "import random; print \"#\"+\"\".join([random.choice(\"0123456789abcdef\") for j in range(6)])"` -gravity center -fill black -weight 700 -pointsize 200 -annotate 0 "$i" "$i.jpg"; done
```

## Resources
- https://github.com/KoRiGaN/Vue2Leaflet
- https://vuematerial.io
- https://www.w3schools.com/html/html5_semantic_elements.asp
- http://jsfiddle.net/a3nvjqvg/
- Drag & Drop
  - https://github.com/chybie/file-upload-vue/blob/master/src/App.vue
  - https://vue-file-upload-1126b.firebaseapp.com/?_sm_au_=iVVtq6QkDF5Fffjs

## Project installation
```
vue create zweierlei.org
babel, typescript, progressive web app, router, vuex, linter, unit & e2e testing
```

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your tests
```
npm run test
```

### Lints and fixes files
```
npm run lint
```

### Run your unit tests
```
npm run test:unit
```
