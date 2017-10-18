import React, { Component } from 'react';
import { Link } from 'react-router-dom';

export default class Nav extends Component {
  render() {
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