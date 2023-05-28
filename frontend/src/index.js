import React from 'react';
import ReactDOM from 'react-dom/client';
import {Routes, Route, BrowserRouter} from "react-router-dom";
import {createBrowserHistory} from "history";
import './index.css';
import App from './components/App';
import Blockchain from "./components/Blockchain";
import ConductTransaction from "./components/ConductTransaction";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<BrowserRouter history={createBrowserHistory()}>
    <Routes>
        <Route path='/' exact element={<App/>}/>
        <Route path='/blockchain' element={<Blockchain/>}/>
        <Route path='/conduct-transaction' element={<ConductTransaction/>}/>
    </Routes>
</BrowserRouter>);
