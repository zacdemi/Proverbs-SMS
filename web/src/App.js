import React from 'react';
import './App.css';
import { MultiStepForm }  from './components/MultiStepForm';
import { Title } from "./components/Title";
import { Container } from 'semantic-ui-react';

function App() {

  return (
    <div className="App">
      <Container style={ {marginTop: 40 }}>
        <Title />
        <MultiStepForm/>
      </Container>
    </div>
  );
}

export default App;