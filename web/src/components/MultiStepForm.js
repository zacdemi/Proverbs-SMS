import React, {useState} from 'react';
import { PhoneForm } from './PhoneForm';
import { ConfirmForm } from './ConfirmForm';
import { PreferencesForm } from './PreferencesForm';

export const MultiStepForm = () => {
    const [step, setStep] = useState(1);

    const nextStep = () => {
        setStep(step + 1)
    }
    return(
             <div>
             {step === 1 && <PhoneForm nextStep={nextStep}/>}
             {step === 2 && <ConfirmForm nextStep={nextStep}/>}
             {step === 3 && <PreferencesForm nextStep={nextStep} />}
            </div>
    )
}