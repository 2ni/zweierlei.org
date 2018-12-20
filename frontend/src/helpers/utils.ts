// utils to delay promise
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
function delay(ms, f) {
  return new Promise(function(resolve) {
    setTimeout(resolve.bind(null, f), ms)
  });
}

export { wait, delay };
