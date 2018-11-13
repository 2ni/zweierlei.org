import * as axios from 'axios';

const BASE_URL = 'http://localhost:8080';

function upload(formData) {
  // console.log(formData.getAll('photos'));
  const requestOptions = {
    method: 'POST',
    body: formData,
  };
  return fetch(`${BASE_URL}/photos/upload`, requestOptions)
    .then(x => {
      return x;
    });
}

/*
function upload(formData) {
    const url = `${BASE_URL}/photos/upload`;
    return axios.post(url, formData)
        // get data
        .then(x => x.data)
        // add url field
        .then(x => x.map(img => Object.assign({},
            img, { url: `${BASE_URL}/images/${img.id}` })));
}
*/

export { upload }
