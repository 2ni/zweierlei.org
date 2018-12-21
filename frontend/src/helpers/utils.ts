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

export { wait, delay };
