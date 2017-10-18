import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Home from './Home';
import Login from './Login';
import Register from './Register';

export default () => (
  <BrowserRouter>
    <Switch>
      <Route exact path="/" render={props => <Home {...props} />} />
      <Route path="/login" render={props => <Login {...props} />} />
      <Route path="/register" render={props => <Register {...props} />} />
    </Switch>
  </BrowserRouter>
);