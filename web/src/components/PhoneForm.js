import React, {useState} from 'react';
import {Form, Button, Message} from 'semantic-ui-react';
import PhoneInput, {isPossiblePhoneNumber} from 'react-phone-number-input';
import flags from 'react-phone-number-input/flags';
import 'react-phone-number-input/style.css';


export const PhoneForm = ({nextStep}) => {
    const [phone, setPhone] = useState();
    const [errors, setErrors] = useState({error:false, message:''});

    const handleSubmit = async() => {
        console.log('Submit Success!')
        console.log(phone)
        console.log(errors)

        //validate
        if (!phone) {
            setErrors({error:true,message:'Phone number can not be blank'})
        }
        else if (!isPossiblePhoneNumber(phone)) {
            setErrors({error:true,message:'Please enter a valid phone number'})
        }
        else {
            setErrors({error:false,message:''})

             const response = await fetch('https://p2r7ot3d2j.execute-api.us-east-1.amazonaws.com/dev/users', {
                 method: 'POST', 
                 headers: {
                     'Content-Type': 'application/json'
                 },
                 body: JSON.stringify({"phone":phone})
             })

             const data = await response.json();
             console.log(data)

             // switch over to next form component
             nextStep()
        }

    }
     
    return  (
        <Form 
            onSubmit={handleSubmit}
            error={errors.error}>
            <PhoneInput
                defaultCountry='US'
                flags={flags}
                value={phone} 
                onChange={setPhone}/>
            <Message
                error
                header='Whoops!'
                content={errors.message}/>
            <Button>Submit</Button>
        </Form>
    )
}