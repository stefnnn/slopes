import React from "react";

const LogoutPage = () => {
  /*
   * Isn't displayed since we have an immediate redirect.
   */
  return (
    <main>
      <h2 className="mb-4">Good bye!</h2>
      <p>You have been logged out successfully</p>
    </main>
  );
};

export default LogoutPage;
