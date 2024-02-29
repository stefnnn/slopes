import React from "react";
import { ServerState, useServer } from "./_server/useServer";

const Home = () => {
  const serverState = useServer();
  const user = serverState.global_state?.logged_in_user;
  const isLoggedIn = !!user;

  return (
    <main>
      <h2 className="mb-4 max-w-[70%] mx-auto">Let's go downhill {user?.email}</h2>
      <div className="flex flex-col align-around">
        {isLoggedIn ? (
          <ShowSlopes serverState={serverState} />
        ) : (
          <a href={serverState.linkGenerator.signupController({})} className="btn self-center">
            Sign up
          </a>
        )}
      </div>
    </main>
  );
};

function ShowSlopes({ serverState }: { serverState: ServerState }) {
  return (
    <div>
      {serverState.items.map((item) => (
        <div key={item.id} className="py-2">
          <div>
            <li>
              {item.description} (
              <a
                className="font-medium text-blue-500"
                href={serverState.linkGenerator.slopeController({
                  slope_id: item.id!,
                })}
              >
                View Slope
              </a>
              )
            </li>
          </div>
        </div>
      ))}{" "}
      <button
        className="btn mt-4"
        onClick={async () => {
          await serverState.new_slope();
        }}
      >
        New Slope
      </button>
    </div>
  );
}

export default Home;
