import React, { useState } from "react";
import { useServer } from "./_server/useServer";

const Page = () => {
  const serverState = useServer();
  const [text, setText] = useState(serverState.description);

  const changeDescription = async (e: React.FormEvent<HTMLFormElement>) => {
    await serverState.update_text({
      slope_id: serverState.id,
      requestBody: {
        description: text,
      },
    });
    setText("bla");
  };
  return (
    <main>
      <h2 className="mb-4">Detail Page</h2>
      <div>
        <strong>Current Description:</strong>
        <p>{serverState.description}</p>
      </div>
      <form className="flex flex-col gap-2" onSubmit={changeDescription}>
        <input
          className="border border-gray-300 rounded px-2 py-1 mt-2"
          type="text"
          value={text}
          placeholder="New Description"
          onChange={(e) => setText(e.target.value)}
        />
        <button className="btn" type="submit">
          Update
        </button>
      </form>
    </main>
  );
};

export default Page;
