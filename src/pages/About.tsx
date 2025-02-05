import { Footer } from "@/components/Footer";
import { Navbar } from "@/components/Navbar";

const About = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="pt-16">
        <section className="py-20 bg-gradient-to-b from-white to-purple-50">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="text-4xl font-bold mb-6 animate-fade-in">
                About RipaPay
              </h1>
              <p className="text-lg text-gray-600 mb-8 animate-fade-in">
                Revolutionizing payments with Qubic blockchain technology
              </p>
            </div>
          </div>
        </section>

        <section className="py-16">
          <div className="container mx-auto px-4">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="space-y-6 animate-fade-in">
                <h2 className="text-3xl font-bold mb-4">Our Mission</h2>
                <p className="text-gray-600">
                  At RipaPay, we're building the future of payments by leveraging
                  the power of the Qubic blockchain. Our mission is to make
                  cryptocurrency payments accessible, secure, and efficient for
                  businesses worldwide.
                </p>
              </div>
              <div className="relative animate-float">
                <img
                  src="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158"
                  alt="Modern technology"
                  className="rounded-lg shadow-xl"
                />
              </div>
            </div>
          </div>
        </section>

        <section className="py-16 bg-purple-50">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto">
              <h2 className="text-3xl font-bold mb-8 text-center animate-fade-in">
                Why Choose RipaPay?
              </h2>
              <div className="grid md:grid-cols-3 gap-8">
                <div className="bg-white p-6 rounded-lg shadow-md animate-fade-in">
                  <h3 className="text-xl font-semibold mb-4">No Monthly Fees</h3>
                  <p className="text-gray-600">
                    We only charge 1.25% per transaction, with no hidden costs or
                    monthly subscriptions.
                  </p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-md animate-fade-in">
                  <h3 className="text-xl font-semibold mb-4">
                    Qubic Technology
                  </h3>
                  <p className="text-gray-600">
                    Powered by the innovative Qubic blockchain for fast and secure
                    transactions.
                  </p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-md animate-fade-in">
                  <h3 className="text-xl font-semibold mb-4">Easy Setup</h3>
                  <p className="text-gray-600">
                    Get started in just 3 simple steps and begin accepting payments
                    immediately.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default About;