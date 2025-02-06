import { Footer } from "@/components/Footer";
import { Navbar } from "@/components/Navbar";
import { ArrowRight, CheckCircle2 } from "lucide-react";

const HowItWorks = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="pt-16">
        <section className="py-20 bg-gradient-to-b from-white to-purple-50">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="text-4xl font-bold mb-6 animate-fade-in">
                How RipaPay Works
              </h1>
              <p className="text-lg text-gray-600 animate-fade-in">
                Start accepting crypto payments in just three simple steps
              </p>
            </div>
          </div>
        </section>

        <section className="py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="grid md:grid-cols-3 gap-8">
                {[
                  {
                    step: 1,
                    title: "Sign Up",
                    description:
                      "Create your RipaPay account with basic information",
                  },
                  {
                    step: 2,
                    title: "Submit Details",
                    description:
                      "Provide your business information and verify your account",
                  },
                  {
                    step: 3,
                    title: "Accept Payments",
                    description:
                      "Start accepting crypto payments from your customers",
                  },
                ].map((item, index) => (
                  <div
                    key={item.step}
                    className="relative p-6 bg-white rounded-lg shadow-md animate-fade-in"
                  >
                    <div className="flex items-center mb-4">
                      <span className="w-8 h-8 flex items-center justify-center bg-ripa-primary text-white rounded-full text-lg font-semibold">
                        {item.step}
                      </span>
                      {index < 2 && (
                        <ArrowRight className="absolute -right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hidden md:block" />
                      )}
                    </div>
                    <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                    <p className="text-gray-600">{item.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="py-16 bg-purple-50">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto">
              <h2 className="text-3xl font-bold mb-8 text-center animate-fade-in">
                Transaction Fees
              </h2>
              <div className="bg-white p-8 rounded-lg shadow-md animate-fade-in">
                <div className="flex items-start space-x-4">
                  <CheckCircle2 className="w-6 h-6 text-green-500 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="text-xl font-semibold mb-2">
                      Simple, Transparent Pricing
                    </h3>
                    <p className="text-gray-600">
                      We believe in keeping things simple. That's why we only
                      charge a 1.25% fee per transaction, with no monthly
                      subscription fees or hidden costs. This helps maintain our
                      ecosystem while keeping costs predictable for your business.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-3xl font-bold mb-8 animate-fade-in">
                Powered by Qubic Blockchain
              </h2>
              <p className="text-lg text-gray-600 mb-8 animate-fade-in">
                RipaPay leverages the power of Qubic blockchain technology to
                provide fast, secure, and efficient payment processing. With
                features like smart contracts and instant settlements, your
                business can operate with confidence in the digital economy.
              </p>
              <div className="grid md:grid-cols-2 gap-8">
                <img
                  src="https://images.unsplash.com/photo-1488590528505-98d2b5aba04b"
                  alt="Technology"
                  className="rounded-lg shadow-xl animate-float"
                />
                <img
                  src="https://images.unsplash.com/photo-1498050108023-c5249f4df085"
                  alt="Code"
                  className="rounded-lg shadow-xl animate-float"
                />
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default HowItWorks;