import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const formSchema = z.object({
	businessName: z.string().min(2, "Business name must be at least 2 characters"),
	country: z.string().min(2, "Please select a country"),
	legalEntityType: z.string().min(2, "Please select an entity type"),
	registrationNumber: z.string().min(2, "Registration number is required"),
	industryType: z.string().min(2, "Please select an industry type"),
});

type BusinessDetailsFormProps = {
	onNext: () => void;
};

export default function BusinessDetailsForm({ onNext }: BusinessDetailsFormProps) {
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
					name="businessName"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Business Name</FormLabel>
							<FormControl>
								<Input placeholder="Enter business name" className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary" {...field} />
							</FormControl>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="country"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Country</FormLabel>
							<Select onValueChange={field.onChange} defaultValue={field.value}>
								<FormControl>
									<SelectTrigger className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary">
										<SelectValue placeholder="Select country" />
									</SelectTrigger>
								</FormControl>
								<SelectContent>
									<SelectItem value="kenya">Kenya</SelectItem>
									<SelectItem value="uganda">Uganda</SelectItem>
									<SelectItem value="tanzania">Tanzania</SelectItem>
								</SelectContent>
							</Select>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="legalEntityType"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Legal Entity Type</FormLabel>
							<Select onValueChange={field.onChange} defaultValue={field.value}>
								<FormControl>
									<SelectTrigger className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary">
										<SelectValue placeholder="Select entity type" />
									</SelectTrigger>
								</FormControl>
								<SelectContent>
									<SelectItem value="sole">Sole Proprietorship</SelectItem>
									<SelectItem value="partnership">Partnership</SelectItem>
									<SelectItem value="corporation">Corporation</SelectItem>
									<SelectItem value="llc">LLC</SelectItem>
								</SelectContent>
							</Select>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="registrationNumber"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Registration Number</FormLabel>
							<FormControl>
								<Input placeholder="Enter registration number" className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary" {...field} />
							</FormControl>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="industryType"
					render={({ field }) => (
						<FormItem>
							<FormLabel className="text-gray-700">Industry Type</FormLabel>
							<Select onValueChange={field.onChange} defaultValue={field.value}>
								<FormControl>
									<SelectTrigger className="border-gray-300 focus:border-ripa-primary focus:ring-ripa-primary">
										<SelectValue placeholder="Select industry type" />
									</SelectTrigger>
								</FormControl>
								<SelectContent>
									<SelectItem value="retail">Retail</SelectItem>
									<SelectItem value="technology">Technology</SelectItem>
									<SelectItem value="finance">Finance</SelectItem>
									<SelectItem value="healthcare">Healthcare</SelectItem>
									<SelectItem value="manufacturing">Manufacturing</SelectItem>
									<SelectItem value="other">Other</SelectItem>
								</SelectContent>
							</Select>
							<FormMessage className="text-red-500" />
						</FormItem>
					)}
				/>

				<Button type="submit" className="w-full bg-ripa-primary hover:bg-ripa-primary/90">Next</Button>
			</form>
		</Form>
	);
}