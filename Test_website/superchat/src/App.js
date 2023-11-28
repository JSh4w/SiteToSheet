import React from 'react';
import './App.css';

import firebase from 'firebase/app';
import 'firebase/firestore';
import 'firebase/auth';

import { useAuthState} from 'react-firebase-hooks/auth';
import{ useCollectionData} from 'react-firebase-hooks/firestore'; 

firebase.initializeApp({
  //your config
  apiKey: "AIzaSyD_yoVtf4yJSThYk6wYlmJa998r7tXv-zI",
  authDomain: "superchat-fbf89.firebaseapp.com",
  projectId: "superchat-fbf89",
  storageBucket: "superchat-fbf89.appspot.com",
  messagingSenderId: "201680541723",
  appId: "1:201680541723:web:1780b00e0951610befc0be",
  measurementId: "G-SVEJQQSWPJ"
})

const auth = firebase.auth();
const firestore = firebase.firestore();

function App() {
  return (
    <div className="App">
      <header className="App-header">

      </header>
    </div>
  );
}

export default App;
