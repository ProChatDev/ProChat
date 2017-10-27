import React, { Component } from 'react';
import Header from './Header';
import Nav from './Nav';

export default class Layout extends Component {
  render() {
    return (
      <div>
        <header className="PC-header">
          <Header />
          <Nav active_link={this.props.active_link} />
        </header>
      </div>
    );
  }
}