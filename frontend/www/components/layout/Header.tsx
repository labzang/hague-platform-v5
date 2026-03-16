"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-sm border-b border-gray-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="text-xl font-bold text-gray-900 hover:text-blue-600 transition-colors">
            Labzang
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-4">
            <a 
              href="https://labzang.github.io" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              <Button variant="outline" size="sm">
                블로그
              </Button>
            </a>
            <Link href="/auth/login">
              <Button variant="outline" size="sm">
                로그인
              </Button>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

