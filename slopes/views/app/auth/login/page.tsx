import React, { useState } from "react";
import { useServer } from "./_server/useServer";
import { HTTPValidationErrorException, LoginInvalidException } from "./_server/actions";
import { LinkComponent, InputComponent, ButtonComponent, ErrorComponent } from "../components";

const LoginPage = () => {
  const serverState = useServer();

  const [isLoadingSubmit, setIsLoadingSubmit] = useState(false);
  const [loginError, setLoginError] = useState<string | undefined>(undefined);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <main>
      <h2>Sign in to your account</h2>
      <div className="mt-2 text-center text-sm text-gray-600">
        If you don't have an account, sign up{" "}
        <LinkComponent href={serverState.linkGenerator.signupController({})}>here.</LinkComponent>
      </div>
      <form className="mt-8 space-y-4 rounded bg-white p-8 shadow">
        {loginError && (
          <ErrorComponent>
            <span>{loginError}</span>
          </ErrorComponent>
        )}
        <InputComponent
          type="email"
          onChange={(e) => {
            setEmail(e.target.value);
          }}
          placeholder="Email"
          value={email}
        />
        <InputComponent
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          value={password}
        />
        <ButtonComponent
          type="submit"
          disabled={isLoadingSubmit}
          onClick={async () => {
            setIsLoadingSubmit(true);

            try {
              await serverState.login({
                requestBody: {
                  username: email,
                  password: password,
                },
              });
              setLoginError(undefined);
              window.location.href = serverState.post_login_redirect;
            } catch (e) {
              if (e instanceof LoginInvalidException) {
                setLoginError(e.body?.invalid_reason);
              } else if (e instanceof HTTPValidationErrorException) {
                setLoginError(e.body?.detail?.[0]?.msg);
              } else {
                throw e;
              }
            } finally {
              setIsLoadingSubmit(false);
            }
          }}
        >
          Login
        </ButtonComponent>
      </form>
    </main>
  );
};

export default LoginPage;
