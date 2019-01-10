/*
 * usage
 * .then(wait(1000)).then(...)
 *
 */
function wait(ms) {
  return (x) => {
    return new Promise((resolve) => setTimeout(() => resolve(x), ms));
  };
}

/*
 * usage
 * delay(1000).then(() => {
 *  // do stuff after 1000mx
 * });
 *
 */
function delay(ms) {
  return new Promise((resolve) => { setTimeout(resolve, ms); });
}

/*
 * filter an object
 * filter_objject({'foo': 'bar', 'mensch': 'meier'}, ['foo']);
 */
function filterObject(input, filter) {
  const filtered = Object.keys(input)
    .filter(key => filter.includes(key))
    .reduce((obj, key) => {
      obj[key] = input[key];
      return obj;
    }, {});

  return filtered;
}

export { wait, delay, filterObject };
