import { useState } from "react";
import API from "../api/api";

function PDFUploader() {

  const [files, setFiles] = useState([]);

  const uploadFiles = async () => {

    if (files.length === 0) {
      alert("Please select at least one PDF");
      return;
    }

    const formData = new FormData();

    for (let file of files) {
      formData.append("files", file);
    }

    try {

      const response = await API.post(
        "/upload",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      alert(
        `Successfully uploaded ${files.length} PDF(s)`
      );

      console.log(response.data);

    } catch (error) {

      console.error(error);

      alert("Upload failed");
    }
  };

  return (

    <div className="bg-[#1a1a1a] p-4 rounded-2xl border border-[#222]">

      <p className="text-sm text-gray-400 mb-3">
        Upload PDFs
      </p>

      <input
        type="file"
        multiple
        accept=".pdf"
        onChange={(e) =>
          setFiles(
            Array.from(e.target.files)
          )
        }
        className="
          w-full
          text-sm
          text-gray-300
          mb-4
        "
      />

      {files.length > 0 && (

        <div className="mb-4">

          <p className="text-green-400 text-sm mb-2">
            {files.length} file(s) selected
          </p>

          <div className="space-y-1">

            {files.map(
              (file, index) => (

                <div
                  key={index}
                  className="
                    text-xs
                    text-gray-400
                    truncate
                  "
                >
                  📄 {file.name}
                </div>

              )
            )}

          </div>

        </div>

      )}

      <button
        onClick={uploadFiles}
        className="
          w-full
          bg-emerald-500
          hover:bg-emerald-600
          transition
          py-2
          rounded-xl
          font-semibold
        "
      >
        Upload
      </button>

    </div>

  );
}

export default PDFUploader;