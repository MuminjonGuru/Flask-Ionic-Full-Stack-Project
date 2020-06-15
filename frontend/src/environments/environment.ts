/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-m-guru',
    audience: 'http://localhost:5000', 
    clientId: '6z07X9iEwo5w73wU1YCurK0S1Ni2L7iR', 
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
