import { useState, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function ChatWindow({
  sessionId,
  messages,
  setMessages
}) {

  const [question, setQuestion] =
    useState("");

  const [compare, setCompare] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const abortControllerRef =
    useRef(null);

  const openPDF = (
    filename,
    page
  ) => {

    const token =
      localStorage.getItem(
        "token"
      );

    const url =
      `http://127.0.0.1:8000/pdf/${encodeURIComponent(
        filename
      )}?token=${token}#page=${page}`;

    window.open(
      url,
      "_blank"
    );

  };

  const sendMessage = async () => {

    if (!question.trim())
      return;

    const currentQuestion =
      question;

    setMessages(prev => [
      ...prev,
      {
        role: "user",
        content: currentQuestion,
        sources: []
      }
    ]);

    setQuestion("");

    setLoading(true);

    setMessages(prev => [
      ...prev,
      {
        role: "assistant",
        content: "",
        sources: []
      }
    ]);

    try {

      const token =
        localStorage.getItem(
          "token"
        );

      const controller =
        new AbortController();

      abortControllerRef.current =
        controller;

      const response =
        await fetch(
          "http://127.0.0.1:8000/chat/stream",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",

              "Authorization":
                `Bearer ${token}`
            },

            signal:
              controller.signal,

            body:
              JSON.stringify({

                question:
                  currentQuestion,

                session_id:
                  sessionId,

                compare:
                  compare

              })

          }
        );

      if (!response.ok) {

        throw new Error(
          "Request failed"
        );

      }

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let buffer = "";

      let fullAnswer = "";

      while (true) {

        const {
          value,
          done
        } =
          await reader.read();

        if (done)
          break;

        buffer +=
          decoder.decode(
            value
          );

        const lines =
          buffer.split("\n");

        buffer =
          lines.pop();

        for (
          const line
          of lines
        ) {

          if (!line.trim())
            continue;

          const data =
            JSON.parse(
              line
            );

          if (
            data.type ===
            "answer"
          ) {

            fullAnswer +=
              data.data;

            setMessages(
              prev => {

                const updated =
                  [...prev];

                updated[
                  updated.length - 1
                ] = {

                  ...updated[
                    updated.length - 1
                  ],

                  content:
                    fullAnswer

                };

                return updated;

              }
            );

          }

          if (
            data.type ===
            "sources"
          ) {

            setMessages(
              prev => {

                const updated =
                  [...prev];

                updated[
                  updated.length - 1
                ] = {

                  ...updated[
                    updated.length - 1
                  ],

                  sources:
                    data.data

                };

                return updated;

              }
            );

          }

        }

      }

    }

    catch (error) {

      if (
        error.name ===
        "AbortError"
      ) {

        console.log(
          "Generation stopped"
        );

      }

      else {

        console.error(
          error
        );

        setMessages(
          prev => {

            const updated =
              [...prev];

            updated[
              updated.length - 1
            ] = {

              ...updated[
                updated.length - 1
              ],

              content:
                "Something went wrong."

            };

            return updated;

          }
        );

      }

    }

    finally {

      abortControllerRef.current =
        null;

      setLoading(false);

    }

  };

  const stopGeneration =
    () => {

      if (
        abortControllerRef.current
      ) {

        abortControllerRef
          .current
          .abort();

      }

    };

  return (

    <div className="flex flex-col h-full">

      <div className="flex justify-between mb-4">

        <h2 className="text-xl font-semibold">
          Chat
        </h2>

        <div className="flex gap-3 items-center">

          <span className="text-gray-400">
            Compare PDFs
          </span>

          <button

            onClick={() =>
              setCompare(
                !compare
              )
            }

            className={`
              w-14
              h-8
              rounded-full
              relative
              ${
                compare
                  ? "bg-emerald-500"
                  : "bg-gray-600"
              }
            `}
          >

            <div

              className={`
                bg-white
                w-6
                h-6
                rounded-full
                absolute
                top-1
                transition-all
                ${
                  compare
                    ? "left-7"
                    : "left-1"
                }
              `}
            />

          </button>

        </div>

      </div>

      <div className="flex-1 overflow-y-auto space-y-6">

        {

          messages.map(
            (
              msg,
              index
            ) => (

              <div

                key={index}

                className={`flex ${
                  msg.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}

              >

                <div

                  className={`max-w-[85%] p-5 rounded-3xl ${
                    msg.role === "user"
                      ? "bg-emerald-500 text-black"
                      : "bg-[#1a1a1a]"
                  }`}

                >

                  {

                    msg.role ===
                    "assistant"

                      ?

                     <ReactMarkdown
                         remarkPlugins={[remarkGfm]}
                     >
                          {msg.content}
                     </ReactMarkdown>

                      :

                      msg.content

                  }

                  {

                    msg.role ===
                      "assistant" &&
                    msg.sources &&
                    msg.sources.length > 0 && (

                      <div className="mt-5">

                        <p className="text-xs text-gray-400 mb-3">

                          Sources

                        </p>

                        {

                          msg.sources.map(
                            (
                              source,
                              idx
                            ) => (

                              <div

                                key={idx}

                                className="
                                  bg-[#222]
                                  border
                                  border-[#333]
                                  rounded-xl
                                  p-4
                                  mb-3
                                "

                              >

                                <div className="flex justify-between items-center mb-2">

                                  <div>

                                    <div className="text-emerald-400 font-medium">

                                      📄 {source.pdf_name}

                                    </div>

                                    <div className="text-xs text-gray-400">

                                      Page {source.page}

                                    </div>

                                  </div>

                                  <button

                                    onClick={() =>
                                      openPDF(
                                        source.pdf_name,
                                        source.page
                                      )
                                    }

                                    className="
                                      bg-emerald-500
                                      text-black
                                      px-3
                                      py-1
                                      rounded-lg
                                      text-sm
                                      font-medium
                                    "

                                  >

                                    Open PDF

                                  </button>

                                </div>

                                {

                                  source.text && (

                                    <div className="
                                      text-sm
                                      text-gray-300
                                      bg-[#181818]
                                      rounded-lg
                                      p-3
                                      mt-2
                                      whitespace-pre-wrap
                                    ">

                                      {source.text}

                                    </div>

                                  )

                                }

                              </div>

                            )
                          )

                        }

                      </div>

                    )

                  }

                </div>

              </div>

            )
          )

        }

      </div>

      <div className="mt-5 flex bg-[#111] border border-[#222] rounded-3xl p-3">

        <input

          value={question}

          onChange={(e) =>
            setQuestion(
              e.target.value
            )
          }

          placeholder="Ask anything..."

          className="
            flex-1
            bg-transparent
            outline-none
          "

          onKeyDown={(e) => {

            if (
              e.key === "Enter" &&
              !loading
            ) {

              sendMessage();

            }

          }}

        />

        {

          loading

            ?

            <button

              onClick={
                stopGeneration
              }

              className="
                bg-red-500
                text-black
                px-8
                rounded-xl
                font-semibold
              "

            >

              Stop

            </button>

            :

            <button

              onClick={
                sendMessage
              }

              className="
                bg-emerald-500
                text-black
                px-8
                rounded-xl
                font-semibold
              "

            >

              Send

            </button>

        }

      </div>

    </div>

  );

}

export default ChatWindow;