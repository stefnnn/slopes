import React from "react";
import linkGenerator from "../_server/links";

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="mx-auto max-w-md mt-4 bg-neutral-100 border-neutral-50 border-2 rounded-xl p-4 shadow-xl">
      <header className="mb-2">
        <h1 className="text-4xl font-extralight">Slopes ⛷️</h1>
        <nav className="flex gap-4 justify-between">
          <a href={linkGenerator.homeController({})} className="underline">
            Home
          </a>
          <div className="flex gap-4">
            <a href={linkGenerator.logoutController({})} className="underline">
              Logout
            </a>
            <a href={linkGenerator.loginController({})} className="underline">
              Login
            </a>
            <a href={linkGenerator.signupController({})} className="underline">
              Signup
            </a>
          </div>
        </nav>
      </header>
      <main>{children}</main>
      <footer className="mt-8">
        <p className="text-center text-neutral-500 text-sm">© Random Dude, 2024</p>
      </footer>
    </div>
  );
};

export default Layout;
