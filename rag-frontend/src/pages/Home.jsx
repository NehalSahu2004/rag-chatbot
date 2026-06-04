import { useState, useEffect } from "react";

import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import API from "../api/api";

function Home() {

  const [sessionId, setSessionId] =
    useState(
      localStorage.getItem(
        "currentSessionId"
      ) ||
      Date.now().toString()
    );

  const [messages, setMessages] =
    useState([
      {
        role: "assistant",
        content:
          "Hello! Upload PDFs and ask me anything.",
        sources: []
      }
    ]);

  useEffect(() => {

    localStorage.setItem(
      "currentSessionId",
      sessionId
    );

  }, [sessionId]);

  useEffect(() => {

    const loadCurrentChat =
      async () => {

        try {

          const response =
            await API.get(
              `/history/${sessionId}`
            );

          if (
            response.data.messages &&
            response.data.messages.length > 0
          ) {

            setMessages(
              response.data.messages
            );

          }

        }

        catch (error) {

          console.log(error);

        }

      };

    loadCurrentChat();

  }, [sessionId]);

  return (

    <div
      className="
        flex
        h-screen
        bg-black
        text-white
        overflow-hidden
      "
    >

      <Sidebar

        sessionId={
          sessionId
        }

        setSessionId={
          setSessionId
        }

        setMessages={
          setMessages
        }

      />

      <div
        className="
          flex-1
          flex
          flex-col
        "
      >

        <div
          className="
            h-[80px]
            border-b
            border-[#222]
            flex
            items-center
            px-8
          "
        >

          <h2
            className="
              text-2xl
              font-semibold
            "
          >

            Multi-PDF RAG Assistant

          </h2>

        </div>

        <div
          className="
            flex-1
            overflow-hidden
            p-6
          "
        >

          <ChatWindow

            sessionId={
              sessionId
            }

            messages={
              messages
            }

            setMessages={
              setMessages
            }

          />

        </div>

      </div>

    </div>

  );

}

export default Home;