import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const formSchema = z.object({
	primaryContactName: z.string().min(2, "Contact name must be at least 2 characters"),
	email: z.string().email("Please enter a valid email address"),
	phoneNumber: z.string().min(10, "Please enter a valid phone number"),
	businessAddress: z.string().min(5, "Please enter a valid business address"),
});

type ContactInformationFormProps = {
	onBack: () => void;
	onNext: () => void;
};

export default function ContactInformationForm({ onBack, onNext }: ContactInformationFormProps) {
	const form = useForm<z.infer<typeof formSchema>>({
		resolver: zodResolver(formSchema),
	});

	const onSubmit = (values: z.infer<typeof formSchema>) => {
		console.log(values);
		onNext();
	};

	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
				<FormField
					control={form.control}
					name="primaryContactName"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Primary Contact Name</FormLabel>
							<FormControl>
								<Input placeholder="Enter contact name" className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary" {...field} />
							</FormControl>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="email"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Email</FormLabel>
							<FormControl>
								<Input type="email" placeholder="Enter email address" className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary" {...field} />
							</FormControl>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="phoneNumber"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Phone Number</FormLabel>
							<FormControl>
								<Input type="tel" placeholder="Enter phone number" className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary" {...field} />
							</FormControl>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="businessAddress"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Business Address</FormLabel>
							<FormControl>
								<Input placeholder="Enter business address" className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary" {...field} />
							</FormControl>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<div className="flex justify-between gap-4">
					<Button type="button" variant="outline" className="border-ripa-primary text-ripa-primary hover:bg-ripa-primary/10" onClick={onBack}>Back</Button>
					<Button type="submit" className="bg-ripa-primary hover:bg-ripa-primary/90">Next</Button>
				</div>
			</form>
		</Form>
	);
}