import React from 'react';
import './App.css';
import { PhoneForm }  from './components/PhoneForm';
import { Container } from 'semantic-ui-react';

function App() {
  /*
  useEffect(() => {
    fetch('/home').then(response => 
      response.json().then(data => {
        console.log(data)
      })
      );

  }, [])
  */

  return (
    <div className="App">
      <Container style={ {marginTop: 40 }}>
        <PhoneForm />
      </Container>
    </div>
  );
}

export default App;