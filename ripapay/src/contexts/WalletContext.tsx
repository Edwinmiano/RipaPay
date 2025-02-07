import { createContext, useContext, useState, ReactNode } from 'react';

interface WalletContextType {
	isConnected: boolean;
	address: string | null;
	balance: string | null;
	connect: () => Promise<void>;
	disconnect: () => void;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

export function WalletProvider({ children }: { children: ReactNode }) {
	const [isConnected, setIsConnected] = useState(false);
	const [address, setAddress] = useState<string | null>(null);
	const [balance, setBalance] = useState<string | null>(null);

	const connect = async () => {
		try {
			// TODO: Implement Qubic wallet connection
			setIsConnected(true);
			setAddress("sample_address"); // Will be replaced with actual wallet address
			setBalance("0.00"); // Will be replaced with actual balance
		} catch (error) {
			console.error('Failed to connect wallet:', error);
		}
	};

	const disconnect = () => {
		setIsConnected(false);
		setAddress(null);
		setBalance(null);
	};

	return (
		<WalletContext.Provider value={{ isConnected, address, balance, connect, disconnect }}>
			{children}
		</WalletContext.Provider>
	);
}

export function useWallet() {
	const context = useContext(WalletContext);
	if (context === undefined) {
		throw new Error('useWallet must be used within a WalletProvider');
	}
	return context;
}