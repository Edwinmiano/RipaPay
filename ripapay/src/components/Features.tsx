import { Wallet, Zap, Shield, Globe } from "lucide-react";

const features = [
  {
    icon: Wallet,
    title: "Multi-Wallet Support",
    description:
      "Connect and manage multiple blockchain wallets seamlessly with our platform.",
  },
  {
    icon: Zap,
    title: "Instant Settlements",
    description:
      "Experience lightning-fast transactions powered by Qubic blockchain technology.",
  },
  {
    icon: Shield,
    title: "Enterprise Security",
    description:
      "Bank-grade security measures to protect your business transactions.",
  },
  {
    icon: Globe,
    title: "Global Reach",
    description:
      "Accept payments from customers worldwide with minimal transaction fees.",
  },
];

export const Features = () => {
  return (
    <section className="py-24 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl font-bold mb-4">
            Why Choose <span className="text-ripa-primary">RipaPay</span>
          </h2>
          <p className="text-gray-600">
            Experience the future of business payments with our comprehensive
            blockchain-powered platform.
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow"
            >
              <feature.icon className="h-12 w-12 text-ripa-primary mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};