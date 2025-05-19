document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const audioFile = document.getElementById('audioFile');
    const method = document.getElementById('method');
    const resultsDiv = document.getElementById('results');
    const googleResult = document.getElementById('googleResult');
    const wav2vec2Result = document.getElementById('wav2vec2Result');
    const googleText = document.getElementById('googleText');
    const wav2vec2Text = document.getElementById('wav2vec2Text');
    const fileName = document.getElementById('fileName');
    const loader = document.getElementById('loader');
    const submitBtn = document.getElementById('submitBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    let currentResultId = null;

    // Handle file selection
    audioFile.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = 'No file selected';
        }
    });

    // Form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!audioFile.files[0]) {
            alert('Please select an audio file first');
            return;
        }

        // Show loader, hide results, disable button
        loader.style.display = 'block';
        resultsDiv.style.display = 'none';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        
        const formData = new FormData();
        formData.append('audio', audioFile.files[0]);
        formData.append('method', method.value);

        try {
            const response = await fetch('/recognize', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            // Hide loader, show results
            loader.style.display = 'none';
            resultsDiv.style.display = 'block';
            
            // Store the result ID for download
            currentResultId = data.result_id;
            
            // Display results based on selected method
            googleResult.style.display = 'none';
            wav2vec2Result.style.display = 'none';
            
            if (data.google) {
                googleResult.style.display = 'block';
                googleText.textContent = data.google;
            }
            
            if (data.wav2vec2) {
                wav2vec2Result.style.display = 'block';
                wav2vec2Text.textContent = data.wav2vec2;
            }
            
            // Show download button
            downloadBtn.style.display = 'inline-block';
            
        } catch (error) {
            alert('Error processing file: ' + error.message);
            console.error('Error:', error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Process Audio';
            loader.style.display = 'none';
        }
    });

    // Download results
    downloadBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (currentResultId) {
            window.location.href = `/download/${currentResultId}`;
        }
    });
});