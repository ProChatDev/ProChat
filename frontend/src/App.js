import React, { Component } from 'react';
import logo from './logo.svg';
//import $ from 'jquery';
import './App.css';
//import Chat from './components/Chat';
import Login from './forms/Login';
import Register from './forms/Register';

export default class App extends Component {
  // constructor() {
  //   super();
  // }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <Login />
        <br />
        <Register />
      </div>
    );
  }
}