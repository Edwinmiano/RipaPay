import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const formSchema = z.object({
	blockchain: z.string().min(2, "Please select a blockchain"),
	walletAddress: z.string().optional(),
	taxId: z.string().optional(),
	taxCountry: z.string().optional(),
});

type CryptoDetailsFormProps = {
	onBack: () => void;
	onSubmit: () => void;
};

export default function CryptoDetailsForm({ onBack, onSubmit: onSubmitProp }: CryptoDetailsFormProps) {
	const form = useForm<z.infer<typeof formSchema>>({
		resolver: zodResolver(formSchema),
	});

	const onSubmit = (values: z.infer<typeof formSchema>) => {
		console.log(values);
		onSubmitProp();
	};

	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
				<FormField
					control={form.control}
					name="blockchain"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Preferred Blockchain</FormLabel>
							<Select onValueChange={field.onChange} defaultValue={field.value}>
								<FormControl>
									<SelectTrigger>
										<SelectValue placeholder="Select blockchain" />
									</SelectTrigger>
								</FormControl>
								<SelectContent>
									<SelectItem value="qubic">Qubic</SelectItem>
									<SelectItem value="solana">Solana (Coming Soon)</SelectItem>
								</SelectContent>
							</Select>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="walletAddress"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Wallet Address (Optional)</FormLabel>
							<FormControl>
								<Input placeholder="Enter wallet address" {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="taxId"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Tax ID / VAT Number (Optional)</FormLabel>
							<FormControl>
								<Input placeholder="Enter tax ID or VAT number" {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name="taxCountry"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Tax Country (Optional)</FormLabel>
							<Select onValueChange={field.onChange} defaultValue={field.value}>
								<FormControl>
									<SelectTrigger>
										<SelectValue placeholder="Select tax country" />
									</SelectTrigger>
								</FormControl>
								<SelectContent>
									<SelectItem value="kenya">Kenya</SelectItem>
									<SelectItem value="uganda">Uganda</SelectItem>
									<SelectItem value="tanzania">Tanzania</SelectItem>
								</SelectContent>
							</Select>
							<FormMessage />
						</FormItem>
					)}
				/>

				<div className="flex justify-between gap-4">
					<Button type="button" variant="outline" onClick={onBack}>Back</Button>
					<Button type="submit">Submit</Button>
				</div>
			</form>
		</Form>
	);
}