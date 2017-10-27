import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Home from './Home';
import Login from './Login';
import Register from './Register';
import Logout from './Logout';

export default () => (
  <BrowserRouter>
    <Switch>
      <Route exact path="/" render={props => <Home {...props} />} />
      <Route path="/login" render={props => <Login {...props} />} />
      <Route path="/register" render={props => <Register {...props} />} />
      <Route path="/logout" render={props => <Logout {...props} />} />
    </Switch>
  </BrowserRouter>
);