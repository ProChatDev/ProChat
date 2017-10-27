import React from 'react';
import ReactDOM from 'react-dom';
import registerServiceWorker from './js/registerServiceWorker';
import './css/index.css';
import App from './js/App';

const app = document.getElementById('root');
ReactDOM.render(<App/>, app);

registerServiceWorker();
