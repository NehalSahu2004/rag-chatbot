import { useEffect, useState } from "react";
import API from "../api/api";

function Sidebar({
  sessionId,
  setSessionId,
  setMessages
}) {

  const [chats, setChats] = useState([]);
  const [files, setFiles] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);

  // =========================
  // LOAD HISTORY
  // =========================

  const loadHistory = async () => {

    try {

      const response =
        await API.get("/history");

      setChats(
        response.data.chats
      );

    }

    catch (error) {

      console.log(error);

    }

  };



  // =========================
  // LOAD DOCUMENTS
  // =========================

  const loadDocuments = async () => {

    try {

      const response =
        await API.get("/documents");

      setDocuments(
        response.data.documents
      );

    }

    catch (error) {

      console.log(error);

    }

  };



  // =========================
  // DELETE DOCUMENT
  // =========================

  const deleteDocument = async (
    filename
  ) => {

    const confirmDelete =
      window.confirm(
        `Delete ${filename}?`
      );

    if (!confirmDelete)
      return;

    try {

      await API.delete(
        `/documents/${encodeURIComponent(filename)}`
      );

      loadDocuments();

      alert(
        "Document deleted successfully"
      );

    }

    catch (error) {

      console.log(error);

      alert(
        "Delete failed"
      );

    }

  };



  // =========================
  // DELETE CHAT
  // =========================

  const deleteChat = async (
    sessionIdToDelete
  ) => {

    const confirmDelete =
      window.confirm(
        "Delete this chat?"
      );

    if (!confirmDelete)
      return;

    try {

      await API.delete(
        `/history/${sessionIdToDelete}`
      );

      loadHistory();

      if (
        sessionIdToDelete ===
        sessionId
      ) {

        newChat();

      }

    }

    catch (error) {

      console.log(error);

      alert(
        "Failed to delete chat"
      );

    }

  };



  // =========================
  // CLEAR ALL HISTORY
  // =========================

  const clearAllHistory = async () => {

    const confirmDelete =
      window.confirm(
        "Delete ALL chat history?"
      );

    if (!confirmDelete)
      return;

    try {

      await API.delete(
        "/history"
      );

      setChats([]);

      newChat();

      alert(
        "History cleared"
      );

    }

    catch (error) {

      console.log(error);

      alert(
        "Failed to clear history"
      );

    }

  };



  // =========================
  // UPLOAD PDF
  // =========================

  const uploadPDF = async () => {

    if (files.length === 0) {

      alert(
        "Please select PDFs"
      );

      return;

    }

    const formData =
      new FormData();

    for (
      let i = 0;
      i < files.length;
      i++
    ) {

      formData.append(
        "files",
        files[i]
      );

    }

    try {

      setUploading(true);

      await API.post(

        "/upload",

        formData,

        {
          headers: {
            "Content-Type":
              "multipart/form-data"
          }
        }

      );

      alert(
        "PDF uploaded successfully"
      );

      setFiles([]);

      loadDocuments();

    }

    catch (error) {

      console.log(error);

      alert(
        "Upload failed"
      );

    }

    setUploading(false);

  };



  // =========================
  // OPEN CHAT
  // =========================

  const openChat = async (
    id
  ) => {

    try {

      const response =
        await API.get(
          `/history/${id}`
        );

      setSessionId(id);

      setMessages(
        response.data.messages
      );

    }

    catch (error) {

      console.log(error);

    }

  };



  // =========================
  // NEW CHAT
  // =========================

  const newChat = () => {

    const id =
      Date.now().toString();

    setSessionId(id);

    setMessages([
      {
        role: "assistant",
        content:
          "Hello! Upload PDFs and ask me anything.",
        sources: []
      }
    ]);

  };



  useEffect(() => {

    loadHistory();

    loadDocuments();

  }, []);



  return (

    <div className="
      w-[320px]
      bg-[#111]
      border-r
      border-[#222]
      h-screen
      flex
      flex-col
    ">

      {/* LOGO */}

      <div className="
        p-6
        border-b
        border-[#222]
      ">

        <h1 className="
          text-3xl
          font-bold
        ">
          TenderGPT
        </h1>

        <p className="
          text-gray-400
          text-sm
        ">
          AI Document Assistant
        </p>

      </div>



      {/* NEW CHAT */}

      <div className="p-4">

        <button

          onClick={newChat}

          className="
          bg-emerald-500
          text-black
          w-full
          py-3
          rounded-xl
          font-semibold
        "
        >

          + New Chat

        </button>

      </div>



      {/* PDF UPLOAD */}

      <div className="
        mx-4
        bg-[#1a1a1a]
        rounded-2xl
        p-4
        border
        border-[#222]
      ">

        <p className="
          text-gray-400
          mb-3
        ">
          Upload PDFs
        </p>

        <input

          type="file"

          multiple

          accept=".pdf"

          onChange={
            (e) =>
              setFiles(
                e.target.files
              )
          }

          className="
          text-sm
          mb-3
        "
        />

        <button

          onClick={uploadPDF}

          className="
          bg-emerald-500
          text-black
          w-full
          py-3
          rounded-xl
          font-semibold
        "
        >

          {
            uploading
              ? "Uploading..."
              : "Upload"
          }

        </button>

      </div>



      {/* DOCUMENTS */}

      <div className="
        p-4
      ">

        <p className="
          text-gray-500
          text-xs
          mb-3
        ">
          DOCUMENTS
        </p>

        {

          documents.map(
            (doc) => (

              <div

                key={doc}

                className="
                bg-[#1a1a1a]
                p-3
                rounded-xl
                mb-2
                flex
                justify-between
                items-center
              "
              >

                <span
                  className="
                  text-sm
                  truncate
                "
                >
                  📄 {doc}
                </span>

                <button

                  onClick={
                    () =>
                      deleteDocument(doc)
                  }

                  className="
                  text-red-400
                "
                >

                  🗑

                </button>

              </div>

            )
          )

        }

      </div>



      {/* HISTORY */}

      <div className="
        flex-1
        overflow-y-auto
        p-4
      ">

        <div className="
          flex
          justify-between
          items-center
          mb-4
        ">

          <p className="
            text-gray-500
            text-xs
          ">
            RECENT CHATS
          </p>

          <button

            onClick={
              clearAllHistory
            }

            className="
            text-red-400
            text-xs
          "
          >

            Clear All

          </button>

        </div>



        {

          chats.map(
            (chat) => (

              <div

                key={
                  chat.session_id
                }

                className="
                bg-[#1a1a1a]
                p-3
                rounded-xl
                mb-3
                flex
                justify-between
                items-center
              "
              >

                <div

                  onClick={
                    () =>
                      openChat(
                        chat.session_id
                      )
                  }

                  className="
                  cursor-pointer
                  flex-1
                "
                >

                  💬 {chat.title}

                </div>

                <button

                  onClick={() =>
                    deleteChat(
                      chat.session_id
                    )
                  }

                  className="
                  text-red-400
                  ml-2
                "
                >

                  🗑

                </button>

              </div>

            )
          )

        }

      </div>

    </div>

  );

}

export default Sidebar;