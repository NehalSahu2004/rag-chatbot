import { useState } from "react";

import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";


function Home() {


  const [sessionId, setSessionId] =
    useState(
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


      {/* SIDEBAR */}


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





      {/* MAIN CHAT AREA */}


      <div
        className="
          flex-1
          flex
          flex-col
        "
      >



        {/* TOP BAR */}


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





        {/* CHAT */}


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