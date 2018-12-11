## Zweierlei
Website implemented with
- vue
- vuecli
- flask-restful
- redis database

### Pre add hook if NOCOMMIT in code
- see https://softwareengineering.stackexchange.com/questions/359861/is-it-possible-to-run-a-git-hook-that-is-executed-when-adding-a-file

create filter in .git/config
```
[filter "nocommit"]
    clean = bash -c 'tee >(cat) | grep -i nocommit -qi && exit 1 || exit 0'
    smudge = cat
    required
```

Register filter in .gitattributes
```
*.txt filter=nocommit
```
