import { Footer } from "@/components/Footer";
import { Navbar } from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Mail, MessageSquare, Phone } from "lucide-react";

const Contact = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="pt-16">
        <section className="py-20 bg-gradient-to-b from-white to-purple-50">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="text-4xl font-bold mb-6 animate-fade-in">
                Contact Us
              </h1>
              <p className="text-lg text-gray-600 animate-fade-in">
                Have questions? We're here to help!
              </p>
            </div>
          </div>
        </section>

        <section className="py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-5xl mx-auto">
              <div className="grid md:grid-cols-2 gap-12">
                <div className="space-y-8 animate-fade-in">
                  <div>
                    <h2 className="text-2xl font-bold mb-6">Get in Touch</h2>
                    <p className="text-gray-600 mb-8">
                      We'd love to hear from you. Please fill out this form and
                      we'll get back to you as soon as possible.
                    </p>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center space-x-4 text-gray-600">
                      <Mail className="w-5 h-5 text-ripa-primary" />
                      <span>support@ripapay.com</span>
                    </div>
                    <div className="flex items-center space-x-4 text-gray-600">
                      <Phone className="w-5 h-5 text-ripa-primary" />
                      <span>+1 (555) 123-4567</span>
                    </div>
                    <div className="flex items-center space-x-4 text-gray-600">
                      <MessageSquare className="w-5 h-5 text-ripa-primary" />
                      <span>Live chat available 24/7</span>
                    </div>
                  </div>
                </div>

                <form className="space-y-6 animate-fade-in">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label
                        htmlFor="firstName"
                        className="text-sm font-medium text-gray-700"
                      >
                        First Name
                      </label>
                      <Input
                        id="firstName"
                        placeholder="John"
                        className="w-full"
                      />
                    </div>
                    <div className="space-y-2">
                      <label
                        htmlFor="lastName"
                        className="text-sm font-medium text-gray-700"
                      >
                        Last Name
                      </label>
                      <Input id="lastName" placeholder="Doe" className="w-full" />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label
                      htmlFor="email"
                      className="text-sm font-medium text-gray-700"
                    >
                      Email
                    </label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="john@example.com"
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-2">
                    <label
                      htmlFor="message"
                      className="text-sm font-medium text-gray-700"
                    >
                      Message
                    </label>
                    <Textarea
                      id="message"
                      placeholder="How can we help you?"
                      className="w-full min-h-[150px]"
                    />
                  </div>

                  <Button className="w-full bg-ripa-primary hover:bg-ripa-primary/90">
                    Send Message
                  </Button>
                </form>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default Contact;