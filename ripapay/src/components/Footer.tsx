import { Link } from "react-router-dom";
import { Github, Twitter, Linkedin } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="bg-white border-t">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-ripa-primary">RipaPay</h3>
            <p className="text-gray-600">
              Revolutionizing payments with Qubic blockchain technology. Simple,
              secure, and efficient.
            </p>
          </div>

          <div className="space-y-4">
            <h4 className="text-sm font-semibold uppercase text-gray-600">
              Quick Links
            </h4>
            <ul className="space-y-2">
              <li>
                <Link
                  to="/about"
                  className="text-gray-600 hover:text-ripa-primary transition-colors"
                >
                  About Us
                </Link>
              </li>
              <li>
                <Link
                  to="/how-it-works"
                  className="text-gray-600 hover:text-ripa-primary transition-colors"
                >
                  How It Works
                </Link>
              </li>
              <li>
                <Link
                  to="/contact"
                  className="text-gray-600 hover:text-ripa-primary transition-colors"
                >
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          <div className="space-y-4">
            <h4 className="text-sm font-semibold uppercase text-gray-600">
              Resources
            </h4>
            <ul className="space-y-2">
              <li>
                <a
                  href="https://qubic.org"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-ripa-primary transition-colors"
                >
                  Qubic.org
                </a>
              </li>
              <li>
                <a
                  href="https://whitepaper.qubic.org"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-ripa-primary transition-colors"
                >
                  Whitepaper
                </a>
              </li>
            </ul>
          </div>

          <div className="space-y-4">
            <h4 className="text-sm font-semibold uppercase text-gray-600">
              Connect
            </h4>
            <div className="flex space-x-4">
              <a
                href="#"
                className="text-gray-600 hover:text-ripa-primary transition-colors"
                aria-label="Github"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="#"
                className="text-gray-600 hover:text-ripa-primary transition-colors"
                aria-label="Twitter"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a
                href="#"
                className="text-gray-600 hover:text-ripa-primary transition-colors"
                aria-label="LinkedIn"
              >
                <Linkedin className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t">
          <p className="text-center text-gray-600">
            © {new Date().getFullYear()} RipaPay. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};