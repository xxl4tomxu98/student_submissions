import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';


const term = "3000";

ReactDOM.render(
    <App term = {term}/>
    , document.getElementById('root'));
registerServiceWorker();
