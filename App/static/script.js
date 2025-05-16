document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("uploadForm");

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById("audioFile");
        const method = document.getElementById("method").value;

        if (!fileInput.files.length) {
            alert("Please select an audio file.");
            return;
        }

        const formData = new FormData();
        formData.append("audio", fileInput.files[0]);
        formData.append("method", method);

        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "Processing...";

        try {
            const response = await fetch("/recognize", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (data.error) {
                resultsDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
            } else {
                let html = "<h2>Results</h2>";
                if (data.google) {
                    html += `<h3>Google</h3><p>${data.google}</p>`;
                }
                if (data.wav2vec2) {
                    html += `<h3>Wav2Vec2</h3><p>${data.wav2vec2}</p>`;
                }
                if (data.result_id) {
                    html += `<a href="/download/${data.result_id}">Download Full Results</a>`;
                }
                resultsDiv.innerHTML = html;
            }
        } catch (error) {
            resultsDiv.innerHTML = `<p style="color:red;">Unexpected error: ${error.message}</p>`;
        }
    });
});
