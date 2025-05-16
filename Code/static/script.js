document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const audioFile = document.getElementById('audioFile').files[0];
    const method = document.getElementById('method').value;

    const formData = new FormData();
    formData.append("audio", audioFile);
    formData.append("method", method);

    const response = await fetch("/recognize", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    const resultsDiv = document.getElementById("results");

    if (result.status === "success") {
        resultsDiv.innerHTML = `
            <h3>Results</h3>
            ${result.google ? `<p><strong>Google:</strong> ${result.google}</p>` : ''}
            ${result.wav2vec2 ? `<p><strong>Wav2Vec2:</strong> ${result.wav2vec2}</p>` : ''}
            <a href="/download/${result.result_id}" download>Download Results</a>
        `;
    } else {
        resultsDiv.innerHTML = `<p style="color:red;">Error: ${result.detail || "Failed to recognize speech"}</p>`;
    }
});
