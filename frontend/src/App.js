import React, { Component } from 'react';
import logo from './logo.svg';
import $ from 'jquery';
import './App.css';
const api = "http://localhost:5000";
const gurl = "/gateway";

class App extends Component {
  constructor() {
    super();
    this.thing = function () {
      $.get(`${api}${gurl}`, function (data, status) {
        console.log(data);
      });
    }
  }
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <script>{this.thing()}</script>
      </div>
    );
  }
}

export default App;
