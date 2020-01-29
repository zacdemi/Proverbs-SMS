import React, {useState} from 'react';
import { Form, Input } from 'semantic-ui-react';

export const PhoneForm = () => {
    const [phone, setPhone] = useState();

    return  (
    <Form>
        <Form.Field>
            <Input 
            placeholder='enter phone number' 
            value={phone} 
            onChange={e =>setPhone(e.target.value)} />
        </Form.Field>
    </Form>
    )
}