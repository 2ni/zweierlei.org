/*
 * handles all api calls concerning stories
 */

import { http } from '@/services';
import router from '@/router';

export const storyService = {
  get,
};

/*
 * Get data from story and attached medias together for now
 */
function get(id: any) {
  const p = new Promise((resolve, reject) => {
    http.get('stories/' + id)
    .then((responseStory) => {
      http.get(responseStory.data.content_url)
      .then((responseMedias) => {
        responseStory.data.medias = responseMedias.data.medias;
        resolve(responseStory);
      })
      .catch((errorMedias) => {
        responseStory.data.medias.msg = errorMedias.response.data.msg;
        resolve(responseStory);
      });
    })
    .catch((errorStory) => {
      reject(errorStory);
    });
  });

  return p;
}
