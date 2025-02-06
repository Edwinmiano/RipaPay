import { Button } from "@/components/ui/button";
import { ArrowRight, Shield } from "lucide-react";
import { useNavigate } from "react-router-dom";

export const Hero = () => {
  const navigate = useNavigate();

  return (
    <div className="relative min-h-screen flex items-center">
      <div className="absolute inset-0 bg-gradient-to-br from-ripa-primary/10 to-transparent" />
      <div className="container mx-auto px-4 pt-16">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <h1 className="text-5xl md:text-6xl font-bold leading-tight">
              Next-Gen{" "}
              <span className="text-ripa-primary">Blockchain Payments</span> for
              Your Business
            </h1>
            <p className="text-xl text-gray-600">
              Powered by Qubic blockchain technology, RipaPay enables secure,
              instant, and low-cost cryptocurrency payments for businesses
              worldwide.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
                <Button
                size="lg"
                className="bg-ripa-primary hover:bg-ripa-primary/90"
                onClick={() => navigate("/business-registration")}
                >
                For Business
                <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
                <Button
                size="lg"
                variant="outline"
                className="border-ripa-primary text-ripa-primary hover:bg-ripa-primary/10"
                onClick={() => navigate("/how-it-works")}
                >
                Learn More
                </Button>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Shield className="h-5 w-5 text-ripa-primary" />
              Enterprise-grade security with blockchain technology
            </div>
          </div>
          <div className="relative animate-float">
            <div className="absolute inset-0 bg-gradient-to-tr from-ripa-primary/20 to-transparent rounded-full blur-3xl" />
            <img
              src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d"
              alt="RipaPay Platform"
              className="relative w-full h-auto rounded-lg shadow-xl"
            />
          </div>
        </div>
      </div>
    </div>
  );
};