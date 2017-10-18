import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import logo from '../logo.svg';
import '../css/App.css';

export default class Header extends Component {
  render() {
    return (
      <div>
        <Link to="/"><img src={logo} className="PC-logo" alt="logo" /></Link>
        <h1 className="PC-title">Welcome to ProChat</h1>
      </div>
    );
  }
}