import React from 'react';
import ReactDOM from 'react-dom/client';
import {Routes, Route, BrowserRouter} from "react-router-dom";
import history from "./history";
import './index.css';
import App from './components/App';
import Blockchain from "./components/Blockchain";
import ConductTransaction from "./components/ConductTransaction";
import TransactionPool from "./components/TransactionPool";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<BrowserRouter history={history}>
    <Routes>
        <Route path='/' exact element={<App/>}/>
        <Route path='/blockchain' element={<Blockchain/>}/>
        <Route path='/conduct-transaction' element={<ConductTransaction/>}/>
        <Route path='/transaction-pool' element={<TransactionPool/>}/>
    </Routes>
</BrowserRouter>);
