import { useState } from "react";
import { Dialog } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import BusinessDetailsForm from "@/components/registration/BusinessDetailsForm";
import ContactInformationForm from "@/components/registration/ContactInformationForm";
import CryptoDetailsForm from "@/components/registration/CryptoDetailsForm";

type RegistrationStep = 1 | 2 | 3;

export default function BusinessRegistration() {
	const [step, setStep] = useState<RegistrationStep>(1);
	const [open, setOpen] = useState(true);

	const renderStep = () => {
		switch (step) {
			case 1:
				return <BusinessDetailsForm onNext={() => setStep(2)} />;
			case 2:
				return (
					<ContactInformationForm 
						onBack={() => setStep(1)} 
						onNext={() => setStep(3)} 
					/>
				);
			case 3:
				return (
					<CryptoDetailsForm 
						onBack={() => setStep(2)} 
						onSubmit={() => {
							// Handle form submission
							setOpen(false);
						}} 
					/>
				);
		}
	};

	return (
		<div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
			<div className="max-w-md mx-auto">
				<Dialog open={open} onOpenChange={setOpen}>
					<div className="text-center">
						<h2 className="mt-6 text-3xl font-extrabold text-gray-900">
							Business Registration
						</h2>
						<p className="mt-2 text-sm text-ripa-primary">
							Step {step} of 3
						</p>
					</div>
					{renderStep()}
				</Dialog>
			</div>
		</div>
	);
}