import { Button } from "@/components/ui/button";
import { useWallet } from "@/contexts/WalletContext";
import { useToast } from "@/components/ui/use-toast";

export function WalletConnect() {
	const { isConnected, address, balance, connect, disconnect } = useWallet();
	const { toast } = useToast();

	const handleConnect = async () => {
		try {
			await connect();
			toast({
				title: "Wallet Connected",
				description: "Successfully connected to Qubic wallet",
			});
		} catch (error) {
			toast({
				title: "Connection Failed",
				description: "Failed to connect to wallet",
				variant: "destructive",
			});
		}
	};

	const handleDisconnect = () => {
		disconnect();
		toast({
			title: "Wallet Disconnected",
			description: "Successfully disconnected from wallet",
		});
	};

	return (
		<div className="flex items-center gap-4">
			{isConnected ? (
				<>
					<div className="text-sm">
						<p>Address: {address?.slice(0, 6)}...{address?.slice(-4)}</p>
						<p>Balance: {balance} QUBIC</p>
					</div>
					<Button variant="destructive" onClick={handleDisconnect}>
						Disconnect
					</Button>
				</>
			) : (
				<Button onClick={handleConnect}>
					Connect Wallet
				</Button>
			)}
		</div>
	);
}