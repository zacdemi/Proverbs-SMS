import React, {useState} from 'react';
import {Form, Button, Message} from 'semantic-ui-react';

export const ConfirmForm = ({nextStep}) => {
    const [errors, setErros] = useState({errors: false, message:""})

    const handleSubmit = () => {
        //api call

        //move to next form
        nextStep()
    }

    return(
        <Form 
        onSubmit={handleSubmit}
        error={errors.error}>
        <Form.Input placeholder='Confirmation Code' />
        <Message
            error
            header='Whoops!'
            content={errors.message}/>
        <Button>Submit</Button>
    </Form>
    )
} 