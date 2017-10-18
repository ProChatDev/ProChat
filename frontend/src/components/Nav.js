import React, { Component } from 'react';
import { Link } from 'react-router-dom';

export default class Nav extends Component {
  isLoggedIn() {
    return (
      localStorage.getItem('email') &&
      localStorage.getItem('username') &&
      localStorage.getItem('id') &&
      localStorage.getItem('token')
    );
  }

  render() {
    if (this.isLoggedIn()) {
      return (
        <nav className="PC-nav">
          <ul>
            <li className="PC-nav-link"><Link to="/logout">Logout</Link></li>
          </ul>
        </nav>
      );
    } else {
      localStorage.clear();
      return (
        <nav className="PC-nav">
          <ul>
            <li className="PC-nav-link"><Link to="/login">Log In</Link></li>
            <li style={{ cursor: 'default' }}>|</li>
            <li className="PC-nav-link"><Link to="/register">Register</Link></li>
          </ul>
        </nav>
      );
    }
  }
}