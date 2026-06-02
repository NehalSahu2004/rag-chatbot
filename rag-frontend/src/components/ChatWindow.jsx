import { useState, useRef } from "react";
import ReactMarkdown from "react-markdown";

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

  const [lastQuestion, setLastQuestion] =
    useState("");

  const abortControllerRef =
    useRef(null);



  const openPDF = (
    filename,
    page
  ) => {

    const url =
      `http://127.0.0.1:9000/files/${encodeURIComponent(filename)}#page=${page}`;

    window.open(
      url,
      "_blank"
    );

  };



  const sendMessage = async (
    customQuestion = null,
    isRegenerate = false
  ) => {

    const currentQuestion =
      customQuestion || question;

    if (!currentQuestion.trim())
      return;

    setLastQuestion(
      currentQuestion
    );



    if (!isRegenerate) {

      const userMessage = {

        role:
        "user",

        content:
        currentQuestion,

        sources:
        []

      };

      setMessages(
        prev => [
          ...prev,
          userMessage
        ]
      );

      setQuestion("");
    }



    setLoading(true);



    const assistantMessage = {

      role:
      "assistant",

      content:
      "",

      sources:
      []

    };



    setMessages(
      prev => [
        ...prev,
        assistantMessage
      ]
    );



    try {

      const controller =
        new AbortController();

      abortControllerRef.current =
        controller;



      const response =
        await fetch(

          "http://127.0.0.1:9000/chat/stream",

          {

            method:
            "POST",

            headers: {

              "Content-Type":
              "application/json"

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



      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let fullAnswer = "";

      let buffer = "";



      while (true) {

        const {
          value,
          done
        }
        =
        await reader.read();



        if (done)
          break;



        buffer +=
          decoder.decode(value);



        const lines =
          buffer.split("\n");

        buffer =
          lines.pop();



        for (
          const line
          of lines
        ) {

          if (
            !line.trim()
          )
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
                ] =
                {

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
                ] =
                {

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

        console.log(
          error
        );

        setMessages(
          prev => {

            const updated =
              [...prev];

            updated[
              updated.length - 1
            ] =
            {

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



    abortControllerRef.current =
      null;

    setLoading(false);

  };



  const stopGeneration = () => {

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

            onClick={
              () =>
                setCompare(
                  !compare
                )
            }

            className={`
            w-14 h-8 rounded-full relative
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

                className={`
                flex
                ${
                  msg.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }
              `}
              >

                <div

                  className={`
                  max-w-[75%]
                  p-5
                  rounded-3xl
                  ${
                    msg.role === "user"
                      ? "bg-emerald-500 text-black"
                      : "bg-[#1a1a1a]"
                  }
                `}
                >

                  {

                    msg.role ===
                      "assistant"

                      ?

                      <>

                        <ReactMarkdown>

                          {msg.content}

                        </ReactMarkdown>

                        {

                          msg.sources?.length > 0 &&

                          <div className="mt-5">

                            <p className="text-gray-400">

                              Sources

                            </p>

                            {

                              msg.sources.map(
                                (
                                  src,
                                  i
                                ) => (

                                  <div

                                    key={i}

                                    className="
                                    border
                                    border-[#333]
                                    rounded-xl
                                    p-3
                                    mt-2
                                  "
                                  >

                                    📄 {src.pdf_name}

                                    <br />

                                    Page {src.page}

                                    <button

                                      onClick={
                                        () =>
                                          openPDF(
                                            src.pdf_name,
                                            src.page
                                          )
                                      }

                                      className="
                                      mt-3
                                      block
                                      bg-emerald-500
                                      text-black
                                      px-4
                                      py-2
                                      rounded-lg
                                    "
                                    >

                                      Open PDF

                                    </button>

                                  </div>

                                )
                              )

                            }

                          </div>

                        }

                        {

                          !loading &&
                          index ===
                          messages.length - 1 &&
                          lastQuestion &&

                          <button

                            onClick={
                              () =>
                                sendMessage(
                                  lastQuestion,
                                  true
                                )
                            }

                            className="
                            mt-4
                            bg-[#222]
                            hover:bg-[#333]
                            px-4
                            py-2
                            rounded-lg
                            text-sm
                          "
                          >

                            🔄 Regenerate

                          </button>

                        }

                      </>

                      :

                      msg.content

                  }

                </div>

              </div>

            )
          )

        }

      </div>



      <div className="
      mt-5
      flex
      bg-[#111]
      border
      border-[#222]
      rounded-3xl
      p-3
      ">

        <input

          value={question}

          onChange={
            e =>
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
        />

        {

          loading ?

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
                () =>
                  sendMessage()
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