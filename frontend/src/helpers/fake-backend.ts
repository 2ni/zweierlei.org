/*
 * http://jasonwatmore.com/post/2018/07/06/vue-vuex-jwt-authentication-tutorial-example
 */

import { fakeUpload } from './';

export function fakeBackend() {
    const users = [{ uid: 1, email: 'test@test.com', password: 'test', firstname: 'Test', lastname: 'User' }];
    const realFetch = window.fetch;
    console.log('backend mocked!');
    window.fetch = (url: any, opts: any) => {
        return new Promise((resolve, reject) => {
            // wrap in timeout to simulate server api call
            setTimeout(() => {

                // authenticate
                if (url.endsWith('/login') && opts.method === 'POST') {
                    // get parameters from post request
                    const params = JSON.parse(opts.body);

                    // find if any user matches login credentials
                    const filteredUsers = users.filter((user) => {
                      return user.email === params.email && user.password === params.password;
                    });

                    if (filteredUsers.length) {
                        // if login details are valid return user details and fake jwt token
                        const user = filteredUsers[0];
                        const responseJson = {
                            uid: user.uid,
                            email: user.email,
                            firstname: user.firstname,
                            lastname: user.lastname,
                            token: 'fake-jwt-token',
                        };
                        resolve({ ok: true, text: () => Promise.resolve(JSON.stringify(responseJson)) });
                    } else {
                        // else return error
                        reject('Email or password is incorrect');
                    }

                    return;
                }

                if (url.endsWith('/photos/upload') && opts.method === 'POST') {
                  // console.log('works', opts.body.getAll('photos'));
                  resolve(fakeUpload(opts.body));
                  return;
                }

                // pass through any requests not handled above
                realFetch(url, opts).then((response) => resolve(response));

            }, 500);
        });
    };
}
